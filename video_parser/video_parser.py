import cv2
import pytesseract
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import re
import matplotlib.pyplot as plt
import concurrent.futures
import time


def process_frame(frame):
  # Prepare a regex pattern to match time strings like '11:22:43 AM'
  time_pattern = re.compile(r'^\d{1,2}:\d{2}:\d{2} (AM|PM)$')

  # Prepare a regex pattern to match decimal numbers
  value_pattern = re.compile(r'^\d+(\.\d+)?$')

  # your frame processing code here
  # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  frame = cv2.bitwise_not(frame)

  frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

  # Use Tesseract to do OCR on the thresholded image
  text = pytesseract.image_to_string(frame)

  # Split the text into lines and extract the data
  lines = text.split('\n')

  if len(lines) >= 2:
    time = lines[0].strip()
    value = lines[1].strip()

    if time_pattern.match(time) and value_pattern.match(value):
      time = pd.to_datetime(time, format='%I:%M:%S %p').time()
      value = float(value)
      return {'Time': time, 'Value': value}
  return None


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

  max_workers = 16
  with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
    frames_to_process = []  # store frames to process

    while True:
      # while frame_num < 600:
      # Read the next frame
      ret, frame = video.read()
      if not ret:
        break

      # 1 frame per second
      if frame_num % (fps // 2) == 0:
        frames_to_process.append(frame)

      frame_num += 1

    # Now, we can use the ThreadPoolExecutor to process the frames
    future_to_frame = {
        executor.submit(process_frame, frame): frame
        for frame in frames_to_process
    }
    for future in concurrent.futures.as_completed(future_to_frame):
      frame = future_to_frame[future]
      try:
        data = future.result()
        if data:
          data_list.append(data)
      except Exception as exc:
        print('%r generated an exception: %s' % (frame, exc))

  # Close the video file
  video.release()

  # Convert the list to a dataframe
  df = pd.DataFrame(data_list)

  # drop time duplicates
  df = df.drop_duplicates(subset='Time')

  # Convert 'Time' column to datetime format
  df['Time'] = pd.to_datetime(
      df['Time'].apply(lambda t: datetime.combine(datetime.today(), t)))

  # Create a date range
  date_range = pd.date_range(start=df['Time'].min(),
                             end=df['Time'].max(),
                             freq='S')

  # Set 'Time' as the index and reindex the DataFrame
  df.set_index('Time', inplace=True)
  df = df.reindex(date_range)

  # Convert the index back to time only if necessary
  df.index = df.index.time

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
  t_start = time.time()
  df = extract_frames('/app/video.mp4')
  print(f'Elapsed time: {time.time() - t_start} seconds')
  print(df.head())
  print(f'Number of rows: {len(df)}')
  print(f'Number of nan rows: {df.Value.isna().sum()}')
  print(f'first time: {df.index[0]}')
  print(f'last time: {df.index[-1]}')

  print(df[df.isna().any(axis=1)])

  # Create and save the plot
  # create_and_save_plot(df)


if __name__ == "__main__":
  main()
