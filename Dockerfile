FROM python:latest

WORKDIR /myapp

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /myapp