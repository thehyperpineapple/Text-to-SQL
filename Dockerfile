# Use the official Python base image with slim version for a lightweight build
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system-level dependencies required for Hugging Face, PyTorch, and transformers
RUN apt-get update && apt-get install -y \
    git \
    wget \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch - this uses the CPU-only version of PyTorch
RUN pip install torch --no-cache-dir

# Install Python dependencies in one step to optimize layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Download and cache the Hugging Face model and tokenizer during the build phase
RUN python -c "from transformers import T5Tokenizer, T5ForConditionalGeneration; \
    T5Tokenizer.from_pretrained('mrm8488/t5-small-finetuned-wikiSQL').save_pretrained('/app/model'); \
    T5ForConditionalGeneration.from_pretrained('mrm8488/t5-small-finetuned-wikiSQL').save_pretrained('/app/model')"

# Copy the rest of the application code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Streamlit-specific command to avoid rerunning unnecessary setup
RUN streamlit config show > /dev/null || true

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
