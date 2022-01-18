
ARG BASE_IMAGE=ubuntu:focal-20200729
FROM ${BASE_IMAGE} as builder

# set the working directory in the container
WORKDIR /

COPY ./grader_service ./grader_service
COPY ./convert ./convert

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    python3 \
    python3-pip
# install dependencies
RUN python3 -m pip install -r ./grader_service/requirements.txt
RUN python3 -m pip install -e ./convert/
RUN python3 -m pip install -e ./grader_service/
# copy the content of the local src directory to the working directory
#RUN ./service/alembic upgrade head
CMD [ "grader-service" ]