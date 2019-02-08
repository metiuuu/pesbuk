FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /pesbuk
WORKDIR /pesbuk
ADD . /pesbuk/
RUN pip install -r requirements.txt