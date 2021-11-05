# Notes from https://www.embeddedonlineconference.com/theatre/Advantages_of_Docker_For_Firmware_Development

FROM ubuntu:20.04

LABEL maintainer="nathancharlesjones@gmail.com"

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y unzip bzip2 \
	gcc-arm-none-eabi=15:9-2019-q4-0ubuntu1

ENV GNU_INSTALL_ROOT /usr/bin/
ENV GNU_PREFIX arm-none-eabi

# Add debugging
RUN apt-get -y install gdb-multiarch