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

# Run the application as a standalone script (One-off task)
CMD ["python", "main.py"]
