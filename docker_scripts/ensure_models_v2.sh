#!/bin/bash
set -e

# Usage: ./ensure_v2_models.sh <MODEL_V2_CHECKPOINT_DIR>
# Example: ./ensure_v2_models.sh /project/tts_files/checkpoints2

MODEL_V2_CHECKPOINT_DIR=${1:-"./checkpoints2"} # Default to ./checkpoints2 if no argument is provided

echo "=== IndexTTS V2 Model Download Script ==="
echo "Model Checkpoint Directory: $MODEL_V2_CHECKPOINT_DIR"

# 这是一个包含了所有 v2 模型文件和子目录的列表
# 这里的 /a/b 格式是为了方便检查文件是否存在
REQUIRED_MODEL_FILES=(
    "bpe.model"
    "config.yaml"
    "feat1.pt"
    "feat2.pt"
    "gpt.pth"
    "qwen0.6bemo4-merge/added_tokens.json"
    "qwen0.6bemo4-merge/chat_template.jinja"
    "qwen0.6bemo4-merge/config.json"
    "qwen0.6bemo4-merge/generation_config.json"
    "qwen0.6bemo4-merge/merges.txt"
    "qwen0.6bemo4-merge/Modelfile"
    "qwen0.6bemo4-merge/model.safetensors"
    "qwen0.6bemo4-merge/special_tokens_map.json"
    "qwen0.6bemo4-merge/tokenizer_config.json"
    "qwen0.6bemo4-merge/tokenizer.json"
    "qwen0.6bemo4-merge/vocab.json"
    "README.md"
    "s2mel.pth"
    "wav2vec2bert_stats.pt"
)

# Function to check if all required model files exist and are not empty
check_v2_models_ready() {
    local all_exist=true
    for file in "${REQUIRED_MODEL_FILES[@]}"; do
        if [ ! -s "$MODEL_V2_CHECKPOINT_DIR/$file" ]; then # -s checks if file exists and is not empty
            all_exist=false
            break
        fi
    done

    if $all_exist; then
        return 0 # Success
    else
        return 1 # Failure
    fi
}

echo "Checking for existing IndexTTS V2 models in $MODEL_V2_CHECKPOINT_DIR..."
if check_v2_models_ready; then
    echo "✅ All required IndexTTS V2 models found and are not empty, skipping download."
else
    echo "📥 IndexTTS V2 models are missing or incomplete, starting download..."

    # Create model directories
    mkdir -p "$MODEL_V2_CHECKPOINT_DIR/qwen0.6bemo4-merge"

    # Function to measure download speed
    measure_speed() {
        local url=$1
        local time_taken=$(curl -o /dev/null -s -w "%{time_total}" "$url")
        echo "$time_taken"
    }

    TEST_FILE="config.yaml"
    BASE_URL_OFFICIAL="https://huggingface.co/IndexTeam/IndexTTS-2/resolve/main"
    BASE_URL_MIRROR="https://hf-mirror.com/IndexTeam/IndexTTS-2/resolve/main"

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

    # Use hf download to download all files
    if command -v huggingface-cli &> /dev/null; then
        echo "Using huggingface-cli to download models..."
        hf download IndexTeam/IndexTTS-2 --local-dir="$MODEL_V2_CHECKPOINT_DIR"

        # Check the result of the hf download command
        if [ $? -ne 0 ]; then
            echo "❌ huggingface-cli download failed. Please check the logs."
            exit 1
        fi
    else
        echo "❌ huggingface-cli not installed. Please install it and retry."
        exit 1
    fi

    if check_v2_models_ready; then
        echo "✅ IndexTTS V2 model download completed successfully."
    else
        echo "❌ IndexTTS V2 model download failed or files are incomplete after download attempt."
        exit 1
    fi
fi

echo "=== V2 Model Download Script Finished ==="