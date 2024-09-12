# Menggunakan image Python sebagai base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install gcc dan dependencies lain yang diperlukan
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Menentukan direktori kerja di dalam container
WORKDIR /app

# Copy file requirements.txt ke dalam container
COPY requirements.txt /app/

# Install dependencies dari requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file dari direktori proyek ke dalam container
COPY . /app/

# Install dependencies menggunakan setup.py
RUN python setup.py build && \
    python setup.py install