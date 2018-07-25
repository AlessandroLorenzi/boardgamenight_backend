FROM python:3.6-alpine

COPY requirements.txt /requirements.txt

RUN apk add --update --no-cache alpine-sdk

RUN apk add --update --no-cache libffi-dev


RUN pip install -r /requirements.txt
RUN pip install gunicorn

COPY src /src

WORKDIR /src

EXPOSE 5000

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]


