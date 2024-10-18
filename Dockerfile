# Use the official Python base image with slim version for a lightweight build
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install Python dependencies in one step to optimize layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Streamlit-specific command to avoid rerunning unnecessary setup
RUN streamlit config show > /dev/null || true

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
