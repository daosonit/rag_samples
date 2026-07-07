docker run --gpus all -p 8000:8000 fedirz/faster-whisper-server:latest-cuda
docker run --gpus all -p 8000:8000 -v ~/.cache/huggingface:/root/.cache/huggingface fedirz/faster-whisper-server:latest-cuda
