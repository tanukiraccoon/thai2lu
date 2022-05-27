# Thai2Lu | Tnk Project
[![Website](https://img.shields.io/website?url=https://thai2lu.tanukishop.net/)](https://thai2lu.tanukishop.net/)
[![Docker Image CI](https://github.com/tanukiraccoon/thai2lu/actions/workflows/docker-image.yml/badge.svg)](https://github.com/tanukiraccoon/thai2lu/actions/workflows/docker-image.yml)
[![GitHub issues](https://img.shields.io/github/issues/tanukiraccoon/thai2lu)](https://github.com/tanukiraccoon/thai2lu/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/tanukiraccoon/thai2lu)](https://github.com/tanukiraccoon/thai2lu/pulls)

โปรแกรมแปลงภาษาไทยเป็นภาษาลู

## Installation
Install with [docker](https://www.docker.com/):
1. Clone the GitHub repository to an empty folder on your local machine:
    ```shell
    git clone https://github.com/tanukiraccoon/thai2lu .
    ```
2. Build
    ```shell
    docker build -t tanukiraccoon/thai2lu .
    ```
3. Run
    ```shell
    docker run -d -p 5000:5000 tanukiraccoon/thai2lu
    ```
4. Stop and Remove
    ```shell
    docker container rm -f tanukiraccoon/thai2lu
    ```
