FROM python:3.7.4
LABEL maintainer ming
ENV PYTHONUNBUFFERED 1
RUN mkdir /api
WORKDIR /api
COPY . /api
RUN pip install -r requirements.txt