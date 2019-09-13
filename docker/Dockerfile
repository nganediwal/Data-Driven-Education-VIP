# Use an official Python runtime as a parent image
FROM dderesearch/default

# Set the working directory to /host
WORKDIR /host

# Add files in /docker to /host
ADD . /host

RUN pip install --upgrade pip
RUN pip install -r pythonrequirements.txt

ENV AWS_CONFIG_FILE /host/.aws/config
ENV AWS_SHARED_CREDENTIALS_FILE /host/.aws/credentials
RUN echo "alias ec2_start='bash /host/sbin/ec2_start.sh'" >> ~/.bashrc
