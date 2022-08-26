FROM python:3.9.7-slim-buster

RUN apt-get update

RUN groupadd -r cosmos && useradd -r -m -g cosmos cosmos 

RUN pip3 install -e .

ENTRYPOINT [ "cosmos" ]
