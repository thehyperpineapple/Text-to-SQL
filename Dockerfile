# Use the official Python base image with slim version for a lightweight build
FROM python:3.9-slim

# Set environment variables to avoid writing .pyc files and to ensure output is flushed immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Upgrade pip and install Python dependencies in one step to optimize layer caching
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && rm -rf ~/.cache/pip  # Clean up pip cache to reduce image size

# Copy the rest of the application code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Streamlit-specific command to avoid rerunning unnecessary setup
RUN streamlit config show > /dev/null || true

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
