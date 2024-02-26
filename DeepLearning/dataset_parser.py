import os
import numpy as np
from shared import dataset_folder, GetRelativePath


class DatasetParser:
  def __init__(self):
    # Dataset constants
    self.angry = "angry"
    self.disgust = "disgust"
    self.fear = "fear"
    self.happy = "happy"
    self.neutral = "neutral"
    self.sad = "sad"
    self.surprise = "surprise"

    self.emotion_list = [self.angry, self.disgust, self.fear, self.happy, self.neutral, self.sad, self.surprise]

    self.emotion_expected_dict = {
      self.angry:   [1, 0, 0, 0, 0, 0, 0],
      self.disgust: [0, 1, 0, 0, 0, 0, 0],
      self.fear:    [0, 0, 1, 0, 0, 0, 0],
      self.happy:   [0, 0, 0, 1, 0, 0, 0],
      self.neutral: [0, 0, 0, 0, 1, 0, 0],
      self.sad:     [0, 0, 0, 0, 0, 1, 0],
      self.surprise:[0, 0, 0, 0, 0, 0, 1],
    }  # fmt: skip

    self.forTesting = "test/"
    self.forLearning = "train/"

  def EmotionNpPointGenerator(self, forWhat: str, EmotionType: str):
    path_to_emotion_entrees = os.path.join(dataset_folder, forWhat, EmotionType)
    files_in_folder = os.listdir(path_to_emotion_entrees)
    for file in files_in_folder:
      # Pre-creating list and defining paths
      result_list = list()
      path_to_file = os.path.join(path_to_emotion_entrees, file)
      path_to_file = GetRelativePath(path_to_file)

      # Reading list of lists as str from file
      with open(path_to_file, "r") as file:
        list_of_lists = file.read()

      # Preparing string for parsing two numbers from sublist
      list_of_lists = list_of_lists[1 : len(list_of_lists) - 1]
      list_of_lists = list_of_lists.split("\n")

      # Parsing from sublist two numbers
      for entry in list_of_lists:
        start_position = 2 if entry[0] == " " else 1
        numbers = entry[start_position:-1].split()
        result_list.append([int(num) for num in numbers])

      yield np.array(result_list)  # returning result as np array for tensor conversion
