FROM python:3.9.7-slim-buster as sdist

LABEL maintainer="develop@hale-terminal.com"
LABEL org.opencontainers.image.title="Cosmos PyPI Wheel"
LABEL org.opencontainers.image.description="PyPI Wheel Builder for Cosmos"
LABEL org.opencontainers.image.url="https://cosmos.io/"
LABEL org.opencontainers.image.source="https://github.com/hale-terminal/cosmos"
LABEL org.opencontainers.image.vendor="Hale Terminal, LLC"
LABEL org.opencontainers.image.authors="develop@hale-terminal.com"

ARG SOURCE_COMMIT
ENV COSMOS_BUILD=${SOURCE_COMMIT:-unknown}
LABEL org.opencontainers.image.revision=$SOURCE_COMMIT
LABEL org.opencontainers.image.licenses="https://github.com/hale-terminal/cosmos/blob/${SOURCE_COMMIT:-master}/LICENSE"

ARG COSMOS_LIGHT_BUILD
ENV COSMOS_LIGHT_BUILD=${COSMOS_LIGHT_BUILD}

RUN echo "COSMOS_LIGHT_BUILD=${COSMOS_LIGHT_BUILD}"

COPY . /usr/src/cosmos/
RUN export YARN_CACHE_FOLDER="$(mktemp -d)" \
    && cd /usr/src/cosmos \
    && python setup.py bdist_wheel \
    && rm -r "$YARN_CACHE_FOLDER" \
    && mv /usr/src/cosmos/dist /dist

# This is the image to be run
FROM python:3.9.7-slim-buster

LABEL maintainer="develop@hale-terminal.com"
LABEL org.opencontainers.image.title="Cosmos"
LABEL org.opencontainers.image.description="Cosmos runtime image"
LABEL org.opencontainers.image.url="https://github.com/hale-terminal/cosmos"
LABEL org.opencontainers.image.documentation="https://github.com/hale-terminal/cosmos"
LABEL org.opencontainers.image.source="https://github.com/hale-terminal/cosmos"
LABEL org.opencontainers.image.vendor="Hale Terminal, LLC"
LABEL org.opencontainers.image.authors="develop@hale-terminal.com"


# add our user and group first to make sure their IDs get assigned consistently
RUN groupadd -r cosmos && useradd -r -m -g cosmos cosmos

# Sane defaults for pip
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Dispatch config params
    COSMOS_CONF=/etc/cosmos

RUN apt-get update && apt-get install -y --no-install-recommends \
    # Needed for fetching stuff
    ca-certificates \
    wget gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=sdist /dist/*.whl /tmp/dist/
RUN set -x \
    && buildDeps="" \
    && apt-get update \
    && apt-get install -y --no-install-recommends $buildDeps \
    # remove internal index when internal plugins are seperated
    && pip install -U /tmp/dist/*.whl \
    && apt-get purge -y --auto-remove $buildDeps \
    # We install run-time dependencies strictly after
    # build dependencies to prevent accidental collusion.
    # These are also installed last as they are needed
    # during container run and can have the same deps w/
    && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000
VOLUME /var/lib/cosmos/files

ENTRYPOINT ["cosmos"]
CMD ["start", "api"]

ARG SOURCE_COMMIT
LABEL org.opencontainers.image.revision=$SOURCE_COMMIT
LABEL org.opencontainers.image.licenses="https://github.com/hale-terminal/cosmos/blob/${SOURCE_COMMIT:-master}/LICENSE"
