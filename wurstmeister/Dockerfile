FROM python:3.7-alpine

WORKDIR /workspace

ADD ./requirements.txt /workspace
ADD ./produce_consume.py /workspace

RUN pip install --no-cache-dir -r /workspace/requirements.txt
