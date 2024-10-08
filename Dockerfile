# DO NOT CHANGE
from 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base-nextflow:v2.0.0

workdir /tmp/docker-build/work/

shell [ \
    "/usr/bin/env", "bash", \
    "-o", "errexit", \
    "-o", "pipefail", \
    "-o", "nounset", \
    "-o", "verbose", \
    "-o", "errtrace", \
    "-O", "inherit_errexit", \
    "-O", "shift_verbose", \
    "-c" \
]
env TZ='Etc/UTC'
env LANG='en_US.UTF-8'

arg DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y wget build-essential python-dev-is-python3

# Install Mambaforge
RUN wget https://github.com/conda-forge/miniforge/releases/latest/download/Mambaforge-Linux-x86_64.sh && \
    bash Mambaforge-Linux-x86_64.sh -b -p /mambaforge && \
    rm Mambaforge-Linux-x86_64.sh

# Create cellxgene environment and install dependencies
RUN /mambaforge/bin/mamba create -n cellxgene --yes python=3.7 && \
    /mambaforge/bin/mamba install -n cellxgene -c conda-forge --yes pip numba==0.52.0 && \
    /mambaforge/bin/mamba run -n cellxgene pip install cellxgene[prepare] && \
    /mambaforge/bin/mamba run -n cellxgene pip install numpy==1.21.6

# Install needed packages
RUN apt-get update && apt-get install -y pigz

# Latch SDK
# DO NOT REMOVE
run pip install latch==2.52.2
run mkdir /opt/latch


# Copy workflow data (use .dockerignore to skip files)

copy . /root/


# Latch workflow registration metadata
# DO NOT CHANGE
arg tag
# DO NOT CHANGE
env FLYTE_INTERNAL_IMAGE $tag

workdir /root
