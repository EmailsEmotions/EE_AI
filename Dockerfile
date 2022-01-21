# syntax=docker/dockerfile:1
FROM python:3.8-buster

WORKDIR application 

# Download dockerize and cache that layer
ENV DOCKERIZE_VERSION v0.6.1
RUN wget -O dockerize.tar.gz https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
RUN tar xzf dockerize.tar.gz
RUN chmod +x dockerize

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
ENTRYPOINT [ "python3", "-u", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5600"]