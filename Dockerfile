# Use Python 3.10 slim image as the base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#
# Create directories for static files and database
RUN mkdir -p /app/staticfiles /app/data

# Copy the entire project into the container
COPY . .

# Make the startup script executable
RUN chmod +x /app/start.sh

# Expose port 8000 for the Django development server
EXPOSE 8000

# Run migrations and start the Django server
CMD ["/app/start.sh"]

