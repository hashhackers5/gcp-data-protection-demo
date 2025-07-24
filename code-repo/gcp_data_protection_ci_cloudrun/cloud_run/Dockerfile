# Use the official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Flask
ENV PYTHONUNBUFFERED True

# Required for Cloud Run to bind to port 8080
ENV PORT 8080

# Expose port
EXPOSE 8080

# Run the web service
CMD ["python", "classifier_service.py"]