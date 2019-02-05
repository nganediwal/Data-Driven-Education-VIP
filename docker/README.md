# Docker Image

https://cloud.docker.com/u/dderesearch/repository/list - our repos. default is the main image, ddetest is for people to play around with fun docker stuff.

## How to use this image

1. Clone the entire git repo to your machine.
2. Download Docker: https://www.docker.com/get-started
  * Note: if you're on Windows 10 Home or earlier, download Docker Toolbox instead: https://docs.docker.com/toolbox/toolbox_install_windows/
2. If you're on Linux or Mac, navigate to the top-level directory (/vip-research/) and run the following command:
```shell
chmod +x ddesetup.sh
```
3. On all systems, in the top-level directory (/vip-research/), run the following command:
```shell
chmod +x ddesetup.sh
```
4. The script should automatically check for updates to this image, pull them from dockerhub, and then launch a container in terminal.

## How to modify this image

**Warning: NEVER EVER put sensitive data of any kind in this /docker/ directory, because it might be packaged into an image and hosted on a public dockerhub server!**
