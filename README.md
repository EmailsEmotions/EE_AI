# EE_AI
# How to run
## Create an environment
Linux
```shell
$ python3 -m venv venv
```
Windows
```command-line
> py -3 -m venv venv
```
## Activate the environment
Linux
```shell
$ . venv/bin/activate
```
Windows
```command-line
> venv\Scripts\activate
```
## Install Flask and Eureka Client
```shell
pip3 install -r requirements.txt
```
## Run app locally
```shell
flask run --host=0.0.0.0 -p 5600
```
## Run app in single container
```shell
docker build -t ai-docker . && docker run -p 5600:80 ai-docker
```