# Pull the exact version you need (solving your 3.8 vs 3.12 issue)
FROM python:3.12-slim

# Set environment variables to prevent Python from writing pyc files
# and to keep logs from being buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project code
COPY . /app/