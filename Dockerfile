FROM python:3.9

RUN mkdir /documaster

WORKDIR /documaster

COPY . /documaster/

RUN pip install --upgrade pip

RUN pip install -r requirements.txt