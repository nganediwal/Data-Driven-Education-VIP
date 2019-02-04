#!/bin/bash

imageName="dderesearch/default:latest"

echo Pulling most recent image of $imageName
docker pull $imageName

successfulPull=$?

if [ $successfulPull != 0 ]; then
	echo ERROR: Unable to pull down the most recent image of $imageName
fi 

echo Starting up new container: The /host directory is connected to the host machine. Use exit to exit.

docker run --rm -p 80:80 -v "$(pwd)":/host/ -it  --entrypoint /bin/bash $imageName