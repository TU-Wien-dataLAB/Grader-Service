
ARG BASE_IMAGE=ubuntu:focal-20200729
FROM ${BASE_IMAGE} as builder

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    python3 \
    python3-pip \
    git \
    tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# INSTALL grader-service
COPY ./grader_service /grader_service
COPY ./convert /convert
COPY ./grader_service.sh /usr/local/bin/grader_service.sh
# install dependencies
RUN python3 -m pip install -r /convert/requirements.txt && \
    python3 -m pip install -r /grader_service/requirements.txt && \
    python3 -m pip install  /convert/ && \
    python3 -m pip install  /grader_service/ && \
    rm -rf /convert/ && \
    rm -rf /grader_service/

 # Create grader-service user
RUN groupadd -g 1000 grader-service && \
    useradd -m -d /var/lib/grader-service -s /bin/nologin -u 1000 -g 1000 grader-service

USER grader-service

WORKDIR /var/lib/grader-service

ENV GRADER_SERVICE_HOST="0.0.0.0"
ENV GRADER_SERVICE_DIRECTORY="/var/lib/grader-service"

ENV GRADER_DB_DIALECT="sqlite"
ENV GRADER_DB_HOST="/var/lib/grader-service/grader.db"

ENV GRADER_AUTOGRADE_IN_PATH="/var/lib/grader-service/convert_in"
ENV GRADER_AUTOGRADE_OUT_PATH="/var/lib/grader-service/convert_out"

ENTRYPOINT ["tini", "-g", "--"]
CMD ["grader_service.sh" ]