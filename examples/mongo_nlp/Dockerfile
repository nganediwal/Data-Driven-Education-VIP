# Use the VIP baseline image
FROM dderesearch/default

# Set the working directory to /host
WORKDIR /host

# Add files in /docker to /host
ADD . /host

ENV AWS_CONFIG_FILE /host/.aws/config
ENV AWS_SHARED_CREDENTIALS_FILE /host/.aws/credentials

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m textblob.download_corpora