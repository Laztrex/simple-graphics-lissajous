FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN adduser --disabled-password --gecos '' qtapp

ENV LIBGL_ALWAYS_INDIRECT=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            python3-pip \
            python3-pyqt5 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/
COPY . .

RUN pip3 install --no-cache-dir -r /tmp/requirements_docker.txt

RUN mkdir -p /files/pics/ && mkdir -p /files/presets/
RUN chown qtapp:qtapp -R /tmp/files

CMD ["python3", "main_lissajous.py"]