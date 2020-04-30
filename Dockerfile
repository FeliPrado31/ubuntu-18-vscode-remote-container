# Base python 2.7 build, inspired by
# https://github.com/crosbymichael/python-docker/blob/master/Dockerfile
FROM ubuntu:18.04

COPY 1.534 /home/minitf
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential \
    ca-certificates \
    libmysqlclient-dev \
    gcc \
    git \
    libpq-dev \
    make \
    python-pip \
    python2.7 \
    python2.7-dev \
    ssh \
    && apt-get autoremove \
    && apt-get clean

RUN pip install -U "setuptools==3.4.1"
RUN pip install -U "pip==1.5.4"
RUN pip install -U "MySQL-python"
RUN pip install -U "psutil"
RUN pip install -U "pip install --upgrade pip"
RUN pip install -U "pip install --upgrade incremental"
RUN pip install -U "pip install Twisted"

EXPOSE 11801
EXPOSE 12801
EXPOSE 13801
EXPOSE 14801

CMD []
ENTRYPOINT ["/bin/bash"]