# Menggunakan Python 3.12-alpine sebagai base image
FROM python:3.12-alpine

# Set environment variable untuk memastikan Python tidak buffering output
ENV PYTHONUNBUFFERED=1

# Install dependencies, termasuk LLVM untuk llvmlite
RUN apk update && \
    apk add --no-cache \
    gcc \
    g++ \
    llvm15-dev \
    llvm15 \
    clang15 \
    libc-dev \
    musl-dev \
    make

# Buat folder kerja di container
WORKDIR /app

# Salin file yang diperlukan ke dalam container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Build C extension untuk ORM
RUN python setup.py build && \
    python setup.py install

# Perintah untuk menjalankan script testing
CMD ["python", "test_jitorm.py"]

# Install dependencies menggunakan setup.py
