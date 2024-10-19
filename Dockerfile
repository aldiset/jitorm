# Gunakan image dasar Python
FROM python:3.11-slim

# Tetapkan direktori kerja
WORKDIR /app

# Salin Pipfile dan Pipfile.lock terlebih dahulu, lalu instal pipenv dan dependencies
COPY Pipfile Pipfile.lock ./

# Instal pipenv dan instal dependencies
RUN pip install --upgrade pip && pip install pipenv \
    && pipenv install --deploy --ignore-pipfile --system \
    && rm -rf /root/.cache/pip /root/.cache/pipenv

# Salin seluruh skrip dan file lainnya
COPY . .

# Tetapkan perintah default untuk menjalankan skrip

#FASTAPI
# EXPOSE 80
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

#run
# CMD [ "python", "run.py" ]