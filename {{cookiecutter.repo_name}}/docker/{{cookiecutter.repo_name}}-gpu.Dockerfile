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

RUN apt update && \
    apt -y install curl git && \
    apt clean

# Use this if deployed outside RunAI
#RUN curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba

ENV PYTHONIOENCODING utf8
ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:$LD_LIBRARY_PATH
ENV PATH "${HOME_DIR}/.local/bin:${PATH}"

USER ${NON_ROOT_USER}
WORKDIR ${HOME_DIR}

COPY --chown=${NON_ROOT_USER}:${NON_ROOT_GID} ${REPO_DIR} {{cookiecutter.repo_name}}

# Install pip requirements
RUN pip install -r {{cookiecutter.repo_name}}/requirements.txt

# Use this if deployed outside RunAI
#RUN micromamba shell init -s bash -r ${HOME_DIR}/micromamba
#RUN micromamba install python=3.12.4 -c defaults -n base -y
#RUN micromamba run -n base pip install -r {{cookiecutter.repo_name}}/requirements.txt
#RUN echo 'alias python="micromamba run -n base python"' >> "${HOME_DIR}/.bashrc"
