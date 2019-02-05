#!/bin/bash

IMAGENAME="dderesearch/default"

# Cleans out any old images (WARNING: If you created your own image it may be destroyed)
docker rmi $IMAGENAME
docker build -t $IMAGENAME docker/

# Note: If you have too many old images run:
# $ docker system prune