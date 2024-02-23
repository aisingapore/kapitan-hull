FROM ubuntu:20.04

ARG DEBIAN_FRONTEND="noninteractive"

ARG NON_ROOT_USER="aisg"
ARG NON_ROOT_UID="2222"
ARG NON_ROOT_GID="2222"
ARG HOME_DIR="/home/${NON_ROOT_USER}"

ARG REPO_DIR="."
ARG CONDA_ENV_FILE="{{cookiecutter.repo_name}}-conda-env.yaml"
ARG CONDA_ENV_NAME="{{cookiecutter.repo_name}}"

# Miniconda arguments
ARG CONDA_HOME="/miniconda3"
ARG CONDA_BIN="${CONDA_HOME}/bin/conda"
ARG CONDA_VER="py310_23.5.2-0"
ARG CONDA_ARCH="Linux-x86_64"
ARG MINICONDA_SH="Miniconda3-${CONDA_VER}-${CONDA_ARCH}.sh"

RUN useradd -l -m -s /bin/bash -u ${NON_ROOT_UID} ${NON_ROOT_USER} && \
    mkdir -p ${CONDA_HOME} && \
    chown -R ${NON_ROOT_USER}:${NON_ROOT_GID} ${CONDA_HOME}

RUN apt-get update && \
    apt-get -y install bzip2 curl wget gcc rsync git vim locales && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8 && \
    apt-get clean

ENV PYTHONIOENCODING utf8
ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"

USER ${NON_ROOT_USER}
WORKDIR ${HOME_DIR}

COPY --chown=${NON_ROOT_USER}:${NON_ROOT_GID} ${REPO_DIR} {{cookiecutter.repo_name}}

# Install Miniconda
RUN curl -O https://repo.anaconda.com/miniconda/$MINICONDA_SH && \
    chmod +x ${MINICONDA_SH} && \
    ./${MINICONDA_SH} -u -b -p ${CONDA_HOME} && \
    rm ${MINICONDA_SH}
ENV PATH ${CONDA_HOME}/bin:${HOME_DIR}/.local/bin:$PATH

# Install conda environment
RUN ${CONDA_BIN} env create -f {{cookiecutter.repo_name}}/${CONDA_ENV_FILE} && \
    ${CONDA_BIN} init bash && \
    ${CONDA_BIN} clean -a -y && \
    echo "source activate ${CONDA_ENV_NAME}" >> "${HOME_DIR}/.bashrc"
