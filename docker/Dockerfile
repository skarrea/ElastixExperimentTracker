FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update 

RUN apt-get update && apt-get install -y software-properties-common gcc && \
	add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y python3.7 python3-distutils python3-pip python3-apt

RUN apt-get -y install wget git sudo
RUN ln -sv /usr/bin/python3 /usr/bin/python
ENV PATH="/usr/bin/python:${PATH}"

# create a non-root user
ARG USER_ID=1000
RUN useradd -m --no-log-init --system  --uid ${USER_ID} appuser -g sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER appuser
WORKDIR /home/appuser


ENV PATH="/home/appuser/.local/bin:${PATH}"
RUN wget https://bootstrap.pypa.io/pip/3.6/get-pip.py && \
	python3 get-pip.py --user && \
	rm get-pip.py

WORKDIR /home/appuser/.elastixSetup
SHELL ["/bin/bash", "-ec"]

RUN git clone https://github.com/skarrea/ElastixExperimentTracker.git .
RUN pip install -r requirements.txt
RUN wget https://github.com/SuperElastix/elastix/releases/download/5.0.0/elastix-5.0.0-linux.tar.bz2
RUN tar -xf elastix-5.0.0-linux.tar.bz2

ENV PATH="/home/appuser/.elastixSetup/bin:${PATH}"
ENV LD_LIBRARY_PATH="/home/appuser/.elastixSetup/lib:${LD_LIBRARY_PATH}"

RUN mkdir ~/elastix
WORKDIR /home/appuser/elastix