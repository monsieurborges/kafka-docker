# Docker Base Image
###########################################################
FROM ubuntu:20.04

LABEL maintainer="Monsieur Borges"
LABEL version="1.0"
LABEL date="2020-06-18"

WORKDIR /workspace

ADD ./requirements.txt /workspace
ADD ./produce_consume.py /workspace

# Create a new Docker Image
###########################################################
ENV DEBIAN_FRONTEND noninteractive
RUN echo "Welcome to the World baby!"\
    # Install dependencies
    #----------------------------------------------------------
    && apt-get update \
    && apt-get --yes --quiet dist-upgrade \
    && apt-get install --yes --quiet --no-install-recommends \
        python3.7 \
        python3-pip \
        librdkafka-dev \
    && pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r /workspace/requirements.txt
