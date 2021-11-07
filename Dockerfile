# Notes from https://www.embeddedonlineconference.com/theatre/Advantages_of_Docker_For_Firmware_Development

FROM ubuntu:20.04

LABEL maintainer="nathancharlesjones@gmail.com"

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update

# Get GNU tools
RUN apt-get install -y build-essential gdb

# Get Arm GCC toolchain and add to PATH
RUN apt-get install -y wget
RUN cd /opt && wget -qO- https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2 | tar -xj
ENV PATH "/opt/gcc-arm-none-eabi-10.3-2021.10/bin:$PATH"

# Get CMake
RUN apt-get install -y python3-pip
RUN pip3 install cmake

# Get other useful tools
RUN apt-get install -y zip git-all ninja-build

# Get sample dependency (mpaland/printf)
# User must copy this folder (and any others) to the correct location once a container is built and started
# Note to self: "cp -a /tmp/. /app" copies all files and directories (recursively) from inside tmp to app
RUN cd /tmp && git clone https://github.com/mpaland/printf.git
