# Video Parser

The Video Parser is a Python script that converts a video file into a time series data file, extracting the time and value information from the video frames.

## Prerequisites

- Python 3.7 or higher
- Docker (for Docker usage)

## Installation

### Docker Installation
1. Clone the repository and navigate to the project directory (this way you have the test .mp4 file):
  ```bash
  git clone https://github.com/stuart-farris/video_parser.git
  cd video_parser
  ```

2. Install Docker on your system following the official Docker installation instructions: [Docker Installation Guide](https://docs.docker.com/get-docker/)

### Non-Docker Installation

1. Install the python package:

  ```bash
  python3 -m pip install video_parser 'git+https://github.com/stuart-farris/video_parser.git@8a4ca186168f7681c33e12b8520e4d2c5d5b1f71'
  ```

2. Clone the repository and navigate to the project directory:
  ```bash
  git clone https://github.com/stuart-farris/video_parser.git
  cd video_parser
  ```

## Usage

### Docker Usage
1. Run the video_parser using the following Docker command:
  ```bash
  docker run \
    -v $PWD/Problem_1/Test_Video.mp4:/app/video.mp4 \
    -v $PWD/results:/app/results \
    sfarris1994/video_parser video_parser
  ```

You can also replace ```$PWD/Problem_1/Test_Video.mp4``` with the path to your video file. The video file should be mounted as a volume inside the Docker container.

The time series data will be extracted from the video file, and a file named output.csv will be created in the current directory.

To run the video parser with GPU acceleration using Docker, use the --gpu argument, as follows:
  ```bash
  docker run \
    -v $PWD/Problem_1/Test_Video.mp4:/app/video.mp4 \
    -v $PWD/results:/app/results \
    --gpus 1 \
    sfarris1994/video_parser video_parser --gpu
  ```
### Non-Docker Usage
1. Navigate to the project directory:
  ```bash
  cd video_parser
  ```
2. Run the video_parser script with the following command:
  ```bash
  video_parser --video Problem_1/Test_Video.mp4
  ```

You can also replace ```Problem_1/Test_Video.mp4``` with the path to your video file.

The time series data will be extracted from the video file, and a file named output.csv will be created in the current directory.

To run the video parser with GPU acceleration, use the --gpu argument, as follows:
```
python video_parser.py Problem_1/Test_Video.mp4 --gpu --video Problem_1/Test_Video.mp4
```

### License
This project is licensed under the MIT License - see the LICENSE file for details.

