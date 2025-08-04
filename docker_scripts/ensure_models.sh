#!/bin/bash
set -e

# Usage: ./ensure_models.sh <MODEL_CHECKPOINT_DIR> <REFERENCE_VOICE_DIR>
# Example: ./ensure_models.sh /app/tts_files/checkpoints /app/tts_files/reference_voices

MODEL_CHECKPOINT_DIR=${1:-"./checkpoints"} # Default to ./checkpoints if no argument is provided
REFERENCE_VOICE_DIR=${2:-"./reference_voices"} # Default to ./reference_voices if no argument is provided

echo "=== IndexTTS Model Download Script ==="
echo "Model Checkpoint Directory: $MODEL_CHECKPOINT_DIR"
echo "Reference Voice Directory: $REFERENCE_VOICE_DIR"

# Create directories
mkdir -p "$MODEL_CHECKPOINT_DIR"
mkdir -p "$REFERENCE_VOICE_DIR"

# Define required model files for IndexTTS-1.5
REQUIRED_MODEL_FILES=(
    "config.yaml"
    "bigvgan_discriminator.pth"
    "bigvgan_generator.pth"
    "bpe.model"
    "dvae.pth"
    "gpt.pth"
    "unigram_12000.vocab"
)

# Function to check if all required model files exist and are not empty
check_models_ready() {
    local all_exist=true
    for file in "${REQUIRED_MODEL_FILES[@]}"; do
        if [ ! -s "$MODEL_CHECKPOINT_DIR/$file" ]; then # -s checks if file exists and is not empty
            all_exist=false
            break
        fi
    done
    return $all_exist
}

echo "Checking for existing IndexTTS models in $MODEL_CHECKPOINT_DIR..."
if check_models_ready; then
    echo "✅ All required IndexTTS models found and are not empty, skipping download."
else
    echo "📥 IndexTTS models are missing or incomplete, starting download..."

    # Function to measure download speed
    measure_speed() {
        local url=$1
        # Use curl to download and get time taken
        local time_taken=$(curl -o /dev/null -s -w "%{time_total}" "$url")
        echo "$time_taken"
    }

    TEST_FILE="config.yaml"
    BASE_URL_OFFICIAL="https://huggingface.co/IndexTeam/IndexTTS-1.5/resolve/main"
    BASE_URL_MIRROR="https://hf-mirror.com/IndexTeam/IndexTTS-1.5/resolve/main"

    echo "⏳ Comparing download speed between official site and mirror..."

    time_official=$(measure_speed "${BASE_URL_OFFICIAL}/${TEST_FILE}")
    time_mirror=$(measure_speed "${BASE_URL_MIRROR}/${TEST_FILE}")

    echo "Official site download time: ${time_official}s"
    echo "Mirror site download time: ${time_mirror}s"

    # Choose the faster endpoint
    if (( $(echo "$time_official < $time_mirror" | bc -l) )); then
        echo "✅ Official site is faster or similar, using official endpoint."
        unset HF_ENDPOINT
    else
        echo "✅ Mirror is faster, using mirror endpoint."
        export HF_ENDPOINT="https://hf-mirror.com"
    fi

    echo "HuggingFace Endpoint set to: ${HF_ENDPOINT:-"https://huggingface.co"}"

    # Try using huggingface-cli for download (recommended)
    if command -v huggingface-cli &> /dev/null; then
        echo "Using huggingface-cli to download models..."
        huggingface-cli download IndexTeam/IndexTTS-1.5 \
          "${REQUIRED_MODEL_FILES[@]}" \
          --local-dir "$MODEL_CHECKPOINT_DIR"

        if [ $? -ne 0 ]; then
            echo "❌ huggingface-cli download failed. Attempting with wget..."
            # Fallback to wget if huggingface-cli fails
            BASE_URL="https://huggingface.co/IndexTeam/IndexTTS-1.5/resolve/main"
            for file in "${REQUIRED_MODEL_FILES[@]}"; do
                echo "Downloading $file with wget..."
                wget "${BASE_URL}/${file}" -O "$MODEL_CHECKPOINT_DIR/${file}" || {
                    echo "❌ Failed to download $file with wget."
                    exit 1
                }
            done
        fi
    else
        echo "huggingface-cli not installed, using wget for download..."
        BASE_URL="https://huggingface.co/IndexTeam/IndexTTS-1.5/resolve/main"
        for file in "${REQUIRED_MODEL_FILES[@]}"; do
            echo "Downloading $file..."
            wget "${BASE_URL}/${file}" -O "$MODEL_CHECKPOINT_DIR/${file}" || {
                echo "❌ Failed to download $file with wget."
                exit 1
            }
        done
    fi

    if check_models_ready; then
        echo "✅ IndexTTS model download completed successfully."
    else
        echo "❌ IndexTTS model download failed or files are incomplete after download attempt."
        exit 1
    fi
fi

# Download/create default reference audio (if not exists)
if [ ! -s "$REFERENCE_VOICE_DIR/default.wav" ]; then
    echo "⚠️ Reference audio file not found or is empty, creating a placeholder..."
    # Create a 1-second silence file as default reference audio using python
    python3 -c "
import numpy as np
import soundfile as sf
import os
output_path = '$REFERENCE_VOICE_DIR/default.wav'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
silence = np.zeros(int(16000 * 1.0))  # 1 second silence, 16kHz
sf.write(output_path, silence, 16000)
print('✅ Default reference audio created at: ' + output_path)
" || echo "⚠️ Failed to create default audio, please manually add default.wav"
else
    echo "✅ Reference audio file found."
fi

echo "=== Model Download Script Finished ==="