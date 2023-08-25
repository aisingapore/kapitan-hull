FROM ubuntu:20.04

ARG DEBIAN_FRONTEND="noninteractive"

ARG NON_ROOT_USER="coder"
ARG NON_ROOT_UID="2222"
ARG NON_ROOT_GID="2222"
ARG HOME_DIR="/home/${NON_ROOT_USER}"

# VSCode Server arguments
ARG CODE_SERVER_VERSION="4.16.1"
ARG CODE_SERVER_BINARY_NAME="code-server_${CODE_SERVER_VERSION}_amd64.deb"

# Miniconda arguments
ARG CONDA_HOME="/miniconda3"
ARG CONDA_BIN="${CONDA_HOME}/bin/conda"
ARG CONDA_VER="py310_23.5.2-0"
ARG CONDA_ARCH="Linux-x86_64"
ARG MINICONDA_SH="Miniconda3-${CONDA_VER}-${CONDA_ARCH}.sh"

RUN apt-get -qqq update && \
    apt-get install -y -qqq --no-install-recommends \
    curl \
    dumb-init \
    htop \
    locales \
    man \
    nano \
    git \
    procps \
    openssh-client \
    sudo \
    vim.tiny \
    lsb-release \
    wget \
    unzip \
    apt-transport-https \
    ca-certificates \
    gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
RUN curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list && \
    apt-get update -qq && \
    apt-get install -y -qq \
    helm

# https://wiki.debian.org/Locale#Manually
RUN sed -i "s/# en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen && \
    locale-gen
ENV LANG=en_US.UTF-8

# Create non-root user and custom miniconda directory
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    useradd -l -m -s /bin/bash -u ${NON_ROOT_UID} ${NON_ROOT_USER} && \
    mkdir -p ${CONDA_HOME} && \
    chown -R ${NON_ROOT_USER}:${NON_ROOT_GID} ${CONDA_HOME} && \
    echo "${NON_ROOT_USER} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd && \
    chmod g+w /etc/passwd

# Install code-server
RUN curl -fOLs "https://github.com/coder/code-server/releases/download/v${CODE_SERVER_VERSION}/${CODE_SERVER_BINARY_NAME}" && \
    sudo dpkg -i ${CODE_SERVER_BINARY_NAME} && \
    rm ${CODE_SERVER_BINARY_NAME}

USER ${NON_ROOT_USER}
WORKDIR ${HOME_DIR}

# Install Miniconda
RUN curl -O "https://repo.anaconda.com/miniconda/${MINICONDA_SH}" && \
    chmod +x ${MINICONDA_SH} && \
    ./${MINICONDA_SH} -u -b -p ${CONDA_HOME} && \
    rm ${MINICONDA_SH}
RUN ${CONDA_HOME}/bin/conda init bash

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    sudo ./aws/install && \
    rm -r awscliv2.zip aws

ENV PATH ${CONDA_HOME}/bin:${HOME_DIR}/.local/bin:${PATH}

ENTRYPOINT ["/usr/bin/code-server", "--disable-telemetry"]
