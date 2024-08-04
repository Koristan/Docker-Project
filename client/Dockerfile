FROM python:latest

WORKDIR /client/

COPY ./req.txt /client/req.txt
RUN pip install --no-cache-dir --upgrade -r /client/req.txt

ADD main.py /client/
ADD config.py /client/
ADD handlers.py /client/
ADD keyboards.py /client/