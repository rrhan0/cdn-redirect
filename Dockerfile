FROM python:3.11-alpine

RUN apk add --no-cache bash \
                       curl \
                       nano

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py .
COPY tests tests

ENTRYPOINT ["python3", "app.py"]