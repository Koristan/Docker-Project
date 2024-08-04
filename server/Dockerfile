
FROM python:latest

WORKDIR /server/

COPY ./req.txt /server/req.txt
RUN pip install --no-cache-dir --upgrade -r /server/req.txt

ADD main.py /server/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "1234"]