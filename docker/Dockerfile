FROM python:3.9.7-slim-buster

RUN apt-get update

COPY . /usr/src/cosmos/
RUN cd /usr/src/cosmos \
    && python setup.py bdist_wheel \
    && mv /usr/src/cosmos/dist /dist

RUN groupadd -r cosmos && useradd -r -m -g cosmos cosmos 

ENTRYPOINT [ "cosmos" ]
