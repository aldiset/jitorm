FROM python:3.12-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip && pip install pipenv \
    && pipenv install --deploy --ignore-pipfile --system \
    && rm -rf /root/.cache/pip /root/.cache/pipenv

COPY . .

CMD [ "python", "main.py" ]
