
ARG BASE_IMAGE=ubuntu:focal-20200729
FROM ${BASE_IMAGE} as builder

# set the working directory in the container
WORKDIR /

COPY ./grader_service ./grader_service
COPY ./convert ./convert

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    python3 \
    python3-pip \
    tini && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install dependencies
RUN python3 -m pip install -r ./grader_service/requirements.txt && \
    python3 -m pip install -e ./convert/ && \
    python3 -m pip install -e ./grader_service/

WORKDIR /grader_service/service/
RUN alembic downgrade base && alembic upgrade head

WORKDIR /
RUN mkdir "grader_service_dir" && \
    mkdir "grader_service_dir/git" && \
    mkdir "./grader_service_dir/convert_in" &&  \
    mkdir "./grader_service_dir/convert_out"

ENV GRADER_SERVICE_HOST="0.0.0.0"
ENV GRADER_SERVICE_DIRECTORY="/grader_service_dir"

ENV JUPYTERHUB_SERVICE_NAME="grader"
ENV JUPYTERHUB_API_TOKEN="7572f93a2e7640999427d9289c8318c0"
ENV JUPYTERHUB_API_URL="http://127.0.0.1:8081/hub/api"
ENV JUPYTERHUB_BASE_URL="/"
ENV JUPYTERHUB_SERVICE_PREFIX=""

ENV GRADER_DB_DIALECT="sqlite"
ENV GRADER_DB_HOST="/grader_service/service/grader.db"

ENV GRADER_AUTOGRADE_IN_PATH="/grader_service_dir/convert_in"
ENV GRADER_AUTOGRADE_OUT_PATH="/grader_service_dir/convert_out"

ENTRYPOINT ["tini", "-g", "--"]
CMD [ "grader-service" ]