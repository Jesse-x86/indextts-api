# 使用你提供的预装了 PyTorch、CUDA 和开发工具的基础镜像
FROM pytorch/pytorch:2.8.0-cuda12.8-cudnn9-devel

# Define environment variables for project paths
ENV INDEX_TTS_ROOT="/app/index-tts"
ENV PROJECT_ROOT="/project"
ENV TTS_FILES_DIR="${PROJECT_ROOT}/tts_files"

# 为 v1 和 v2 模型分别定义目录
ENV MODEL_CHECKPOINT_DIR="${TTS_FILES_DIR}/checkpoints"
ENV MODEL_V2_CHECKPOINT_DIR="${TTS_FILES_DIR}/checkpoints2"

ENV REFERENCE_VOICE_DIR="${TTS_FILES_DIR}/reference_voices"
ENV VOICE_OUTPUTS_DIR="${TTS_FILES_DIR}/outputs"

ENV API_PORT="8198"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    git-lfs \
    ffmpeg \
    bc \
    wget \
    curl \
    bzip2 \
    ca-certificates \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Set up uv for dependency management
RUN pip install --no-cache-dir uv

# Create all necessary directories
RUN mkdir -p ${INDEX_TTS_ROOT} \
           ${PROJECT_ROOT} \
           ${TTS_FILES_DIR} \
           ${MODEL_CHECKPOINT_DIR} \
           ${MODEL_V2_CHECKPOINT_DIR} \
           ${REFERENCE_VOICE_DIR} \
           ${VOICE_OUTPUTS_DIR}

# Clone the original index-tts repository and set up the environment
WORKDIR ${INDEX_TTS_ROOT}
RUN git clone https://github.com/index-tts/index-tts.git . && \
    git lfs pull

# Install dependencies using uv
RUN uv sync

# Copy your local project files into the new project root
WORKDIR ${PROJECT_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ${PROJECT_ROOT}

# Make your entrypoint script executable
RUN chmod +x ./docker_scripts/entry_point.sh
RUN chmod +x ./docker_scripts/ensure_models.sh

# Expose the port for your API
EXPOSE ${API_PORT}

# Set the entrypoint to your local script
ENTRYPOINT ["./docker_scripts/entry_point.sh"]