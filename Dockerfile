FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /tmp/
COPY . /tmp/

RUN adduser --disabled-password --gecos '' app

ENV LIBGL_ALWAYS_INDIRECT=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            python3-pip \
            python3-pyqt5

RUN pip3 install --no-cache-dir -r /tmp/requirements_docker.txt && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /files/pics && mkdir -p /files/presets
RUN chmod -R 777 /files/pics && chmod -R 777 /files/presets

CMD ["python3", "main_lissajous.py"]