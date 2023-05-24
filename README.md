# Video Parser

The Video Parser is a Python script that converts a video file into a time series data file, extracting the time and value information from the video frames.

## Prerequisites

- Python 3.7 or higher
- Poetry (for non-Docker installation)

## Installation

### Docker Installation

1. Install Docker on your system following the official Docker installation instructions: [Docker Installation Guide](https://docs.docker.com/get-docker/)

### Non-Docker Installation

1. Install Poetry by running the following command:

  ```bash
  pip install poetry
  ```

2. Clone the repository and navigate to the project directory:
  ```bash
  git clone <repository_url>
  cd video_parser
  ```

3. Install the project dependencies with Poetry:
  ```bash
  poetry install
  ```

## Usage

### Docker Usage
1. Run the video_parser using the following Docker command:
  ```bash
  docker run -v <path_to_video_file>:/app/video.mp4 video-parser
  ```

Replace <path_to_video_file> with the path to your video file. The video file should be mounted as a volume inside the Docker container.

The time series data will be extracted from the video file, and a file named output.csv will be created in the current directory.

### Non-Docker Usage
1. Activate the virtual environment created by Poetry:
  ```bash
  poetry shell
  ```
2. Run the video_parser script with the following command:
  ```bash
  python video_parser.py <path_to_video_file>
  ```

Replace <path_to_video_file> with the path to your video file.

The time series data will be extracted from the video file, and a file named output.csv will be created in the current directory.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

