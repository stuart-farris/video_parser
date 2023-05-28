"""
This script processes a video file to extract time and value pairs from frames.

The main steps are as follows:
1. A video file is loaded, and the frames are extracted.
2. Each frame is processed using EasyOCR to extract text parts.
3. Text parts are then processed to extract time and value pairs.
4. The resulting data is then plotted and saved as a PNG file. 
5. Additionally, the data is also saved in a CSV file.

This script can optionally utilize GPU acceleration for processing frames 
by using the '--gpu' command line argument.

Usage: python3 script_name.py --gpu
"""
import os
import cv2
import pandas as pd
from datetime import datetime
import re
import matplotlib.pyplot as plt
import time
import easyocr
import argparse
from typing import List, Dict, Union, Optional, List


def process_text_parts(
    text_parts: List[List[Union[List[List[int]], str, float]]]
) -> List[Dict[str, Union[datetime.time, float]]]:
  """
  Process text parts and extracts time and value information from them.

  Parameters:
  text_parts (List[List[Union[List[List[int]], str, float]]]): 
      List of lists containing the position, text, and confidence of detected text in each frame.
  
  Returns:
  List[Dict[str, Union[datetime.time, float]]]: List of dictionaries containing time and value for each frame.
  """
  # Prepare a regex pattern to match time strings in various formats
  time_pattern = re.compile(r'^\d{1,2}[:.;]?\d{2}[:.;]?\d{2}[:.;]? ?(AM|PM)$',
                            re.IGNORECASE)

  # Prepare a regex pattern to match decimal numbers
  value_pattern = re.compile(r'^\d+(\.\d+)?$')

  data_list = []

  for part in text_parts:
    # Each part should contain two lines, one for time and one for value
    if len(part) >= 2:
      time_text = part[0][1].strip()
      value_text = part[1][1].strip()

      if time_pattern.match(time_text) and value_pattern.match(value_text):
        # Ensure that time is properly formatted
        normalized_time_text = normalize_time(time_text)
        time = pd.to_datetime(normalized_time_text, format='%I:%M:%S %p').time()
        value = float(value_text)
        data_list.append({'Time': time, 'Value': value})

  return data_list


def normalize_time(time_text: str) -> str:
  """
    Normalizes time text to have proper separators and format.

    Parameters:
    time_text (str): Text that represents time.
    
    Returns:
    str: Time text in normalized format.
    """
  # Replace dots with colons
  time_text = time_text.replace('.', ':')
  time_text = time_text.replace(';', ':')

  # Ensure there is a space before AM/PM
  if "AM" in time_text.upper():
    time_text = time_text.upper().replace("AM", " AM").strip()
  elif "PM" in time_text.upper():
    time_text = time_text.upper().replace("PM", " PM").strip()

  # If there's an extra colon (more than 2), remove it
  while time_text.count(':') > 2:
    pos = time_text.rfind(':')  # find last occurrence
    time_text = time_text[:pos] + time_text[pos + 1:]

  # If the number of colons is less than 2 (complete time string should have 2 colons),
  # assume the colon is missing between minutes and seconds, and insert it.
  if time_text.count(':') < 2:
    # Find the position of the existing colon
    pos = time_text.find(':')
    # Insert a colon between minutes and seconds
    time_text = time_text[:pos + 3] + ':' + time_text[pos + 3:]

  return time_text


def extract_frames(video_path: str,
                   use_gpu: Optional[bool] = False) -> pd.DataFrame:
  """
    Extract frames from video and process OCR data to return DataFrame.

    Parameters:
    video_path (str): Path to the video file.
    use_gpu (bool): Flag indicating if GPU should be used for OCR.

    Returns:
    pd.DataFrame: DataFrame with time and value extracted from video frames.
    """
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

  batch_size = 128  # Adjust this based on your GPU's capabilities
  print(f'Loading EasyOCR model')
  reader = easyocr.Reader(['en'], gpu=use_gpu)  # English, using GPU or not
  frames_to_process = []  # store frames to process

  while True:
    # Read the next frame
    ret, frame = video.read()
    if not ret:
      break

    # 1 frame per second
    if frame_num % fps == 0:
      frames_to_process.append(frame)

    frame_num += 1

  # Close the video file
  video.release()

  print(f'\nNumber of frames to process: {len(frames_to_process)}')

  # extract text from frames
  text_parts = reader.readtext_batched(frames_to_process, batch_size=batch_size)

  # parse text into time and value
  data_list = process_text_parts(text_parts)

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


from typing import Optional


def create_and_save_plot(df: pd.DataFrame, path: str = '/app/results') -> None:
  """
    Creates and saves the plot of the DataFrame.

    Parameters:
    df (pd.DataFrame): Data to be plotted.
    path (str): Directory where the plot will be saved.

    Returns:
    None
    """
  os.makedirs(path, exist_ok=True)

  # Create a figure and an axes
  fig, ax = plt.subplots(figsize=(18, 6), constrained_layout=True)

  # Plot the data
  df.plot(kind='line', ax=ax, linewidth=1, color='black')

  # Set the title and labels
  ax.set_title('Time Series of Value', fontsize=14, fontweight='bold')
  ax.set_xlabel('Time', fontsize=12, fontweight='bold')
  ax.set_ylabel('Value', fontsize=12, fontweight='bold')

  # Set the grid
  ax.grid(True, which='both', color='grey', linewidth=0.5)
  ax.set_facecolor('white')

  # Set the spines (the lines surrounding the subplot) to be visible and with some style
  ax.spines['left'].set_color('black')
  ax.spines['left'].set_linewidth(0.5)
  ax.spines['bottom'].set_color('black')
  ax.spines['bottom'].set_linewidth(0.5)
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)

  # Set the tick parameters
  ax.tick_params(axis='both', colors='black')

  # Save the plot as a png file
  plt.savefig(path + '/time_series.png', dpi=300, bbox_inches='tight')


def save_csv(df: pd.DataFrame, path: str = '/app/results') -> None:
  """
    Saves the DataFrame as a CSV.

    Parameters:
    df (pd.DataFrame): DataFrame to be saved.
    path (str): Directory where the CSV will be saved.

    Returns:
    None
    """
  os.makedirs(path, exist_ok=True)
  df.to_csv(path + '/time_series.csv')


def main(use_gpu: Optional[bool] = False) -> None:
  """
    Main function to run the script.

    Parameters:
    use_gpu (bool): Whether to use GPU for processing or not.

    Returns:
    None
    """
  t_start = time.time()
  df = extract_frames('/app/video.mp4', use_gpu)

  # print some results
  print(f'Total run time: {time.time() - t_start} seconds')
  print(f'\nTime series dataframe')
  print(df.head())
  print(f'Number of rows: {len(df)}')
  print(f'Number of bad reads: {df.Value.isna().sum()}')
  print(f'first time: {df.index[0]}')
  print(f'last time: {df.index[-1]}')

  # print where nans exist
  print('\nTimes with bad reads:')
  print(df[df.isna().any(axis=1)])

  # Create and save the plot
  create_and_save_plot(df)

  # save csv
  save_csv(df)


if __name__ == "__main__":
  # Create the parser
  parser = argparse.ArgumentParser(description='Process a video file.')

  # Add the arguments
  parser.add_argument('--gpu',
                      dest='use_gpu',
                      action='store_true',
                      help='Use GPU-accelerated frame processing')

  # Parse the
  args = parser.parse_args()

  # Call the main function with the parsed arguments
  main(use_gpu=args.use_gpu)