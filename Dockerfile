# Use PyTorch image as the base image
FROM pytorch/pytorch

# Set the environment to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Set the maintainer
LABEL maintainer="sfarris@sep.stanford.edu"

# Configure apt and install packages
RUN apt-get update -y && \
    apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-dev \
    git \
    # cleanup
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists

# Install Tesseract and its dependencies
RUN apt-get update -y && \
    apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev x11-apps && \
    apt-get clean && \
    apt-get autoremove 

# Install poetry
RUN pip install poetry

# Disable creation of virtual environments by poetry
RUN poetry config virtualenvs.create false

# Define the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Build the project and install it
RUN cd /app && poetry build && pip install dist/*.tar.gz

RUN chmod -R 777 /app/results

# Set the entrypoint script
# ENTRYPOINT ["python3","video_parser"]




