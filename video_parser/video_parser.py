import cv2
import pytesseract
import pandas as pd
from datetime import datetime
import argparse
from tqdm import tqdm
import re
import matplotlib.pyplot as plt


def extract_frames(video_path):
  # Load the video
  video = cv2.VideoCapture(video_path)
  print('Video loaded successfully')

  fps = int(video.get(cv2.CAP_PROP_FPS))
  print(f'FPS: {fps}')

  total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
  print(f'Total frames: {total_frames}')

  # Initialize the frame number and create empty list to hold data
  frame_num = 0
  data_list = []

  progress_bar = tqdm(
      total=int(total_frames),
      ncols=100,
      dynamic_ncols=True,
  )

  # Prepare a regex pattern to match time strings like '11:22:43 AM'
  time_pattern = re.compile(r'^\d{1,2}:\d{2}:\d{2} (AM|PM)$')

  # Prepare a regex pattern to match decimal numbers
  value_pattern = re.compile(r'^\d+(\.\d+)?$')

  # while True:
  while frame_num < 500:
    # Read the next frame
    ret, frame = video.read()
    if not ret:
      break

    # 1 frame per second
    if frame_num % (fps // 2) == 0:
      # Convert the frame to grayscale
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      # Use Tesseract to do OCR on the thresholded image
      text = pytesseract.image_to_string(frame)

      # Split the text into lines and extract the data
      lines = text.split('\n')

      # Make sure we have at least two lines (time and value)
      if len(lines) >= 2:
        time = lines[0].strip()
        value = lines[1].strip()

        # Check if the time and value are in the expected formats
        if time_pattern.match(time) and value_pattern.match(value):
          # Convert the time string to a datetime object
          time = pd.to_datetime(time, format='%I:%M:%S %p').time()

          # Convert the value to float
          value = float(value)

          # Append the data to the list
          data_list.append({'Time': time, 'Value': value})

    # Increment the frame number
    frame_num += 1
    progress_bar.update(1)

  # Close the progress bar
  progress_bar.close()

  # Close the video file
  video.release()

  # Convert the list to a dataframe
  df = pd.DataFrame(data_list)

  # drop time duplicates
  df = df.drop_duplicates(subset='Time')

  # Return the dataframe
  return df


def create_and_save_plot(df):
  # Create a plot
  df.plot(x='Time', y='Value', kind='line', figsize=(10, 6))

  # Label the axes
  plt.xlabel('Time')
  plt.ylabel('Value')

  # Save the plot as a png file
  plt.savefig('time_series_plot.png')


def main():
  parser = argparse.ArgumentParser(description="Convert video to time series")
  parser.add_argument("video_path", help="Path of the video file to process")
  args = parser.parse_args()

  print(args.video_path)

  df = extract_frames(args.video_path)
  print(df)

  # Convert the 'Time' column to datetime format
  df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.time

  # Create and save the plot
  create_and_save_plot(df)


if __name__ == "__main__":
  main()
