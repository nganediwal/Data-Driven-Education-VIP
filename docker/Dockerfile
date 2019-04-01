# Use an official Python runtime as a parent image
FROM ubuntu:18.04
ENV DEBIAN_FRONTEND noninteractive
# Define environment variable
ENV VIP_DOCKER_IMAGE_VERSION 1.2.0

# Set the working directory to /host
WORKDIR /host

# Add files in /docker to /host
ADD . /host

RUN apt-get update
RUN apt-get install -y \
    gnupg2 \
    curl \
    wget \
    bzip2 \
    git-core \
    postgresql \
    postgresql-contrib \
    python3-pip \
    mongodb

# Aliases for python3
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

# Install Anaconda
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.python.org -r pythonrequirements.txt

ENV AWS_CONFIG_FILE /host/.aws/config
ENV AWS_SHARED_CREDENTIALS_FILE /host/.aws/credentials
RUN echo "alias ec2_start='bash /host/sbin/ec2_start.sh'" >> ~/.bashrc

# Run app.py when the container launches
#CMD ["python", "test.py"]