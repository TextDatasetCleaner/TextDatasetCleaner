FROM python:3.7-slim as build

WORKDIR /build/

COPY src/ src/
COPY setup.py setup.py
COPY README.md README.md

RUN apt-get update && \
    apt-get install -yq --no-install-recommends build-essential=12.6 && \
    python -m pip install --upgrade pip && \
    pip install --no-cache --target deps/ --upgrade .

FROM python:3.7-slim

WORKDIR /tdc/

ENV PYTHONPATH=/opt/tdc/deps/ \
    PATH=/opt/tdc/deps/bin/:${PATH}

COPY --from=build /build/deps/ /opt/tdc/deps/
COPY scripts/clean-all-files.sh /usr/bin/tdc-all-files
COPY config.yml /tdc/config.yml

RUN mkdir -p /tdc/input/ && mkdir -p /tdc/output/ && \
    chmod +x /usr/bin/tdc-all-files

CMD [ "tdc-all-files" ]
