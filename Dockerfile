FROM python:3.8.2-buster

RUN mkdir /app

COPY . /app

RUN pip install -r /app/requirements.txt

CMD [ "python", "-u", "/app/main.py" ]
