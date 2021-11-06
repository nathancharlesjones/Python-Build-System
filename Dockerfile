# Notes from https://www.embeddedonlineconference.com/theatre/Advantages_of_Docker_For_Firmware_Development

FROM ubuntu:20.04

LABEL maintainer="nathancharlesjones@gmail.com"

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
	build-essential \
	gdb \
	gcc-arm-none-eabi=15:9-2019-q4-0ubuntu1 \
	gdb-multiarch \
	zip \
	git-all

RUN cd /app && git clone https://github.com/mpaland/printf.git
