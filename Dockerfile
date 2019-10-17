FROM python:3.6.8

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip && \
    pip3 install --default-timeout=100 -r requirements.txt

ENV FLASK_APP wrapper

ENTRYPOINT ["bash"]
