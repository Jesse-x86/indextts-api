# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Define environment variables for project paths
ENV INDEX_TTS_ROOT="/app/index-tts"
ENV PROJECT_ROOT="/project"
ENV TTS_FILES_DIR="${PROJECT_ROOT}/tts_files"
ENV MODEL_CHECKPOINT_DIR="${TTS_FILES_DIR}/checkpoints"
ENV REFERENCE_VOICE_DIR="${TTS_FILES_DIR}/reference_voices"
ENV VOICE_OUTPUTS_DIR="${TTS_FILES_DIR}/outputs"

ENV API_PORT="8198"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    wget \
    curl \
    bzip2 \
    ca-certificates \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set up global pip and install necessary libraries for download
RUN pip install --no-cache-dir huggingface_hub soundfile

# Create all necessary directories
RUN mkdir -p ${INDEX_TTS_ROOT} \
           ${PROJECT_ROOT} \
           ${TTS_FILES_DIR} \
           ${MODEL_CHECKPOINT_DIR} \
           ${REFERENCE_VOICE_DIR} \
           ${VOICE_OUTPUTS_DIR}

# Clone the original index-tts repository
WORKDIR ${INDEX_TTS_ROOT}
RUN git clone https://github.com/index-tts/index-tts.git .

# Install the cloned project as an editable package
RUN pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118 --no-cache-dir
RUN pip install -e . --no-cache-dir

# Copy your local project files into the new project root
WORKDIR ${PROJECT_ROOT}
COPY . ${PROJECT_ROOT}

# Make your entrypoint script executable
RUN chmod +x ./docker_scripts/entry_point.sh
RUN chmod +x ./docker_scripts/ensure_models.sh

# Expose the port for your API
EXPOSE ${API_PORT}

# Set the entrypoint to your local script
ENTRYPOINT ["./docker_scripts/entry_point.sh"]