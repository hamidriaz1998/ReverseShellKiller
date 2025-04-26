# Base image
FROM python:3.13-slim

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV GEMINI_API_KEY=${GEMINI_API_KEY}
ENV EMAIL_USER=${EMAIL_USER}
ENV EMAIL_PASS=${EMAIL_PASS}

# Expose port (optional)
EXPOSE 8000

# Command to run when container starts
CMD ["uv", "run", "main.py", "--use-llm"]