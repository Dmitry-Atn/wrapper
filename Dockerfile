FROM ubuntu:bionic

COPY . /

RUN sudo apt-get update && \
    sudo apt install python-pip3 && \
    pip3 install -r requirements.txt

