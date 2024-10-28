FROM python:3.10-slim-buster

ARG SERVICE_NAME
ENV SERVICE_NAME ${SERVICE_NAME:-api}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH="/opt:${PYTHONPATH}"

WORKDIR /opt

RUN pip install --upgrade pip
COPY ./requirements-$SERVICE_NAME.txt ./requirements-common.txt ./
RUN pip install -r ./requirements-$SERVICE_NAME.txt -r ./requirements-common.txt

COPY balanced_backend ./balanced_backend

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

# For some reason this is giving permission denied errors in k8s but not in compose???
#RUN useradd -m icon
#RUN chown icon:icon -R /opt
#USER icon

ENTRYPOINT ./entrypoint.sh $SERVICE_NAME
