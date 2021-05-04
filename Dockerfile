FROM ubuntu:18.04

WORKDIR /tmp/

ENV DEBIAN_FRONTEND=noninteractive

RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

ENV LIBGL_ALWAYS_INDIRECT=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            python3-pip \
            python3-pyqt5

COPY . /tmp/

RUN pip3 install --no-cache-dir -r /tmp/requirements_docker.txt && \
    rm -rf /var/lib/apt/lists/*

CMD ["python3", "main_lissajous.py"]