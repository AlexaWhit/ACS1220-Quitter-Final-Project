# Use the official Python image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Create necessary directories
RUN mkdir -p /app/instance

# Set environment variables
ENV PYTHONPATH=/app

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]