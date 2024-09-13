FROM python:3.12-slim

ARG DEBIAN_FRONTEND="noninteractive"

ARG NON_ROOT_USER="aisg"
ARG NON_ROOT_UID="2222"
ARG NON_ROOT_GID="2222"
ARG HOME_DIR="/home/${NON_ROOT_USER}"

ARG REPO_DIR="."

RUN useradd -l -m -s /bin/bash -u ${NON_ROOT_UID} ${NON_ROOT_USER}

RUN apt update && \
    apt -y install curl git && \
    apt clean

ENV PYTHONIOENCODING utf8
ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"
ENV PATH "${HOME_DIR}/.local/bin:${PATH}"

USER ${NON_ROOT_USER}
WORKDIR ${HOME_DIR}

COPY --chown=${NON_ROOT_USER}:${NON_ROOT_GID} ${REPO_DIR} {{cookiecutter.repo_name}}

# Install pip requirements
RUN pip install -r {{cookiecutter.repo_name}}/requirements.txt
RUN pip install -r {{cookiecutter.repo_name}}/pytorch-cpu-requirements.txt