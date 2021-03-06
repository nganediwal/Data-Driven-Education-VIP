#!/bin/bash

IMAGENAME="dderesearch/default"
RESEARCHDIR=$PWD

echo Starting up new container: The /host directory is connected to the host machine. Use exit to exit.
docker run --rm -p 127.0.0.1:80:8080/tcp -v "$RESEARCHDIR":/host/ -it  --entrypoint /bin/bash $IMAGENAME