FROM python:3.7.9-alpine2.12

RUN apt-get update

RUN groupadd -r cosmos && useradd -r -m -g cosmos cosmos 

RUN pip3 install -e .

ENTRYPOINT [ "cosmos" ]
