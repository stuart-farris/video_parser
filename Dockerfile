# Use an official Ubuntu runtime as a parent image
FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

# Set the maintainer
LABEL maintainer="your-email@example.com"

# Update the system
RUN apt-get update -y && \
    apt-get upgrade -y

# Install Tesseract and its dependencies
RUN apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev x11-apps && \
    apt-get clean && \
    apt-get autoremove 

# Install Python 3 and pip
RUN apt-get install -y python3-pip

# Upgrade pip
RUN pip3 install --upgrade pip

# Install poetry
RUN pip3 install poetry

# Disable creation of virtual environments by poetry
RUN poetry config virtualenvs.create false

# Define the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Build the project and install it
RUN poetry build && pip install dist/*.tar.gz

# Set the entrypoint script
# ENTRYPOINT ["video_parser"]




