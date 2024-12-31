FROM python:3.10-slim

# Install required system packages
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Expose port 8000
EXPOSE 8002

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
