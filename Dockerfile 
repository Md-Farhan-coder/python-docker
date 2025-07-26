# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Expose the port Flask runs on
EXPOSE 8080

# Start the app
CMD ["python", "app.py"]
