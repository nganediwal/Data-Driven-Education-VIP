# Use an official Python runtime as a parent image
FROM python:3.7-slim

# Define environment variable
ENV VIP_DOCKER_IMAGE_VERSION 1.1.0

# Set the working directory to /host
WORKDIR /host

# Copy the current directory contents into the container at /host
ADD . /host

RUN apt-get update
RUN apt-get install gnupg2 -y

# Install mongodb
RUN apt-get install curl -y
RUN curl https://www.mongodb.org/static/pgp/server-4.0.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list
RUN apt-get update
RUN apt-get install -y mongodb-org

# Adds colors to terminal and aws config files to ~/.bash_rc
RUN echo "export LS_OPTIONS='--color=auto'" >> ~/.bashrc
RUN echo "alias ls='ls \$LS_OPTIONS'" >> ~/.bashrc
RUN echo "export AWS_CONFIG_FILE=/host/.aws/config" >> ~/.bashrc
RUN echo "export AWS_SHARED_CREDENTIALS_FILE=/host/.aws/credentials" >> ~/.bashrc
RUN echo "alias ec2_start='bash /host/sbin/ec2_start.sh'" >> ~/.bashrc

# Installs PostgreSQL
RUN bash apt.postgresql.org.sh
RUN apt-get install postgresql-11 pgadmin4 -y
# RUN apt-get update && apt-get install postgresql-11 pgadmin4
# RUN apt-get update && apt-get install -y apt-transport-https && apt-get install -y r-base

# Installs python libraries
RUN pip install --trusted-host pypi.python.org -r pythonrequirements.txt

EXPOSE 5050

# Make port 80 available to the world outside this container
#EXPOSE 80

# Run app.py when the container launches
#CMD ["python", "test.py"]