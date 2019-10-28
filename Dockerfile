FROM python:3.6.8-slim

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install --default-timeout=100 -r requirements.txt && \
    python3 resnet50_download.py && \
    chmod +x serve

ENV FLASK_APP wrapper

ENTRYPOINT ["bash"]
