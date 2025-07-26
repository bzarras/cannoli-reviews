FROM --platform=linux/arm64 public.ecr.aws/amazonlinux/amazonlinux:2023

# Set working directory
WORKDIR /app

# Install system dependencies including Python 3.11
RUN dnf update -y && dnf install -y \
    python3.11 \
    python3.11-pip \
    python3.11-devel \
    gcc \
    && dnf clean all

# Create symlink for python and pip
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/pip3.11 /usr/bin/pip

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and database
COPY . .

# Note: Running as root for simplicity

# Expose port 8001
EXPOSE 8001

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"] 
