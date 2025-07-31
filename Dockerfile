# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Define environment variables for model paths
ENV INDEX_TTS_ROOT="/app/index-tts"
ENV TTS_FILES_DIR="/project/tts_files"
ENV MODEL_CHECKPOINT_DIR="${TTS_FILES_DIR}/checkpoints"
ENV REFERENCE_VOICE_DIR="${TTS_FILES_DIR}/reference_voices"

# Install system dependencies
# Added 'curl' for huggingface-cli installation check, and 'python3-pip' (though python:3.10-slim usually has it)
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    wget \
    curl \
    bzip2 \
    ca-certificates \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set up global pip and install huggingface-cli for model download
# Note: This is installed globally before conda to ensure 'huggingface-cli' is available for the download script.
RUN pip install --no-cache-dir huggingface_hub soundfile

# Create the base directory for your project files and models
# This ensures that volume mounts can target these specific paths cleanly.
RUN mkdir -p ${INDEX_TTS_ROOT} \
           ${MODEL_CHECKPOINT_DIR} \
           ${REFERENCE_VOICE_DIR}

# Copy the model download script and make it executable
COPY download_models.sh /usr/local/bin/download_models.sh
RUN chmod +x /usr/local/bin/download_models.sh

# Execute the model download script, passing the target directories as arguments.
# This step is placed early to leverage Docker's build cache.
# If you mount volumes for ${MODEL_CHECKPOINT_DIR} and ${REFERENCE_VOICE_DIR},
# the script will check for existing files and skip downloads.
RUN download_models.sh "${MODEL_CHECKPOINT_DIR}" "${REFERENCE_VOICE_DIR}"

# Clone the index-tts repository into its designated location
WORKDIR ${INDEX_TTS_ROOT}
RUN git clone https://github.com/index-tts/index-tts.git .

# Install Python dependencies for IndexTTS
# First, install PyTorch (GPU version, adjust if CPU only)
RUN pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir

# Install Miniconda for pynini and then activate base environment to install pynini via conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p /opt/conda && \
    rm /tmp/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV PATH="/opt/conda/bin:${PATH}"

# Activate base environment and install pynini and WeTextProcessing
RUN conda install -c conda-forge pynini==2.1.6 -y && \
    pip install WeTextProcessing --no-deps --no-cache-dir

# Install IndexTTS as an editable package
RUN pip install -e . --no-cache-dir

# Optional: Copy your application's requirements.txt and install them
# If you have a requirements.txt in your local project root, assuming it's sibling to Dockerfile:
# COPY ./your_app_requirements.txt ${INDEX_TTS_ROOT}/your_app_requirements.txt
# RUN pip install -r ${INDEX_TTS_ROOT}/your_app_requirements.txt --no-cache-dir

# Set the default working directory for future commands and when the container runs
WORKDIR ${INDEX_TTS_ROOT}

# Define a default command to run when the container starts (example)
# You might want to replace this with a command that starts your application or an interactive shell.
# CMD ["python", "indextts/infer.py"] # Example: running the inference script
# 或者你可能想在启动时使用一个启动脚本来整合所有的检查和启动逻辑，类似你提供的第二个脚本。
# CMD ["/bin/bash", "/app/startup.sh"]