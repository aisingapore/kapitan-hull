# Use this if deployed outside RunAI
#FROM nvcr.io/nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04
FROM python:3.12-slim

ARG DEBIAN_FRONTEND="noninteractive"

ARG NON_ROOT_USER="aisg"
ARG NON_ROOT_UID="2222"
ARG NON_ROOT_GID="2222"
ARG HOME_DIR="/home/${NON_ROOT_USER}"

ARG REPO_DIR="."

RUN useradd -l -m -s /bin/bash -u ${NON_ROOT_UID} ${NON_ROOT_USER}

RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub

RUN apt update && \
    apt -y install curl git && \
    apt clean

ENV PYTHONIOENCODING utf8
ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:$LD_LIBRARY_PATH
ENV PATH "./.local/bin:${PATH}"

USER ${NON_ROOT_USER}
WORKDIR ${HOME_DIR}

COPY --chown=${NON_ROOT_USER}:${NON_ROOT_GID} ${REPO_DIR} {{cookiecutter.repo_name}}

# Install pip requirements
RUN pip install -r {{cookiecutter.repo_name}}/requirements.txt
