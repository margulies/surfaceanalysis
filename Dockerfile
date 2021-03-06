FROM ubuntu:16.04
MAINTAINER Daniel Margulies <daniel.margulies@gmail.com>

RUN apt-get update
RUN apt-get install -y python-dev
RUN apt-get install -y python-pip

ENV MYVAR mything

RUN pip install numpy boutiques nibabel pandas cython
RUN pip install surfdist

COPY surfaceanalysis.py /opt/surfaceanalysis.py
