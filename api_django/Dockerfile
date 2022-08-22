FROM python:3.8

ENV PYTHONUNBUFFERD 1

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install binutils libproj-dev gdal-bin

RUN apt install gdal-bin python3-gdal python3-gdal

RUN apt-get -y update
RUN apt-get -y install cron
#RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get -y update && apt-get -y install libgl1

WORKDIR /api_django

COPY requirements.txt requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

