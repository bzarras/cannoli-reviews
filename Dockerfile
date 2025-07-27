FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Create a virtual environment
RUN uv venv

# Install Python dependencies
RUN uv pip install --no-cache-dir -r requirements.txt

# Copy application code and database
COPY . .

# Note: Running as root for simplicity

# Expose port 8001
EXPOSE 8001

# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"] 
