FROM nvidia/cuda:12.1.0-base-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Pre-download the model weights to the container image
RUN python3 -c "from transformers import AutoTokenizer, AutoModelForCausalLM; \
    tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-1.5B-Instruct'); \
    model = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-1.5B-Instruct')"

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV IS_DOCKER=1
EXPOSE 8000

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
