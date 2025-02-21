FROM python:3.10-slim

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

ARG ENV
ENV ENV $ENV

ARG CONNECTION_STR
ENV CONNECTION_STR $CONNECTION_STR

EXPOSE 8000

CMD [ "python3", "main.py" ]