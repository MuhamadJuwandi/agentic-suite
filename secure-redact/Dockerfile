# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (Apify expects 80 usually, or we can use the env var)
ENV PORT=8000
EXPOSE 8000

# Run the application
# CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000"]

# For Apify, we might want a wrapper script to handle input/output if running as a standalone script,
# but if running as a web server actor:
CMD ["uvicorn", "api.index:app", "--host", "0.0.0.0", "--port", "8000"]
