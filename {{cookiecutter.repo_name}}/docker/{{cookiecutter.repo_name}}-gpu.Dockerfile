# Comment this out if deployed within Run:ai
FROM nvcr.io/nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04

# Use this if deployed within Run:ai
#FROM python:3.12-slim

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

# Comment this out if deployed within Run:ai
RUN curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba

ENV PYTHONIOENCODING=utf8
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
ENV PATH="${HOME_DIR}/.local/bin:${PATH}"

USER ${NON_ROOT_USER}
WORKDIR ${HOME_DIR}

COPY --chown=${NON_ROOT_USER}:${NON_ROOT_GID} ${REPO_DIR} {{cookiecutter.repo_name}}

# Comment this out if deployed within Run:ai
RUN micromamba shell init -s bash -r ${HOME_DIR}/micromamba
RUN micromamba install python=3.12.9 -c defaults -n base -y
RUN micromamba run -n base pip install -r {{cookiecutter.repo_name}}/requirements.txt
RUN mkdir -p ${HOME_DIR}/.local/bin
RUN ln -sf ${HOME_DIR}/micromamba/bin/python ${HOME_DIR}/.local/bin

# Use this if deployed outside Run:ai
#RUN pip install -r {{cookiecutter.repo_name}}/requirements.txt
