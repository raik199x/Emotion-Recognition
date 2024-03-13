import os
import cv2


class DatasetParser:
  def __init__(self, path_to_dataset_folder: str):
    self.dataset_path = path_to_dataset_folder
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

    # Dataset info
    self.forTesting = "test/"
    self.forLearning = "train/"

    # Memory management
    self.learning_set_dict = dict()
    self.testing_set_dict = dict()

  def GetAmountOfFilesInFolder(self, path: str) -> int:
    return len(os.listdir(path))

  def ReloadEmotion(self, forWhat: str, emotion_type: str) -> None:
    full_path = os.path.join(self.dataset_path, forWhat, emotion_type)
    # Reading emotion
    current_emotion_list = list()  # Preparing list for all images in this emotion
    files_in_folder = os.listdir(full_path)
    for file in files_in_folder:
      image = cv2.imread(os.path.join(full_path, file), cv2.IMREAD_GRAYSCALE)
      current_emotion_list.append(image)

    if forWhat == self.forLearning:
      self.learning_set_dict[emotion_type] = current_emotion_list
    elif forWhat == self.forTesting:
      self.testing_set_dict[emotion_type] = current_emotion_list

  def ParseFolderWithEmotions(self, folder_with_emotions: str) -> dict():
    """Parses a folder of emotions and returns a dictionary of emotions to lists of images.

    This function iterates over every emotion in the folder, checks if the emotion exists, and if so,
    loads all the images in the emotion into a list. The list of images is then saved to a dictionary
    with the emotion as the key.

    Args:
      folder_with_emotions: The path to the folder containing the emotions.

    Returns:
      A dictionary of emotions to lists of images.
    """
    emotions_dict = dict()
    for emotion in self.emotion_list:  # iterating over every emotion in folder
      path_to_current_emotion = os.path.join(folder_with_emotions, emotion)

      if not os.path.exists(path_to_current_emotion):
        continue  # If emotion was not founded, just skip

      current_emotion_list = list()  # Preparing list for all images in this emotion
      files_in_folder = os.listdir(path_to_current_emotion)
      for file in files_in_folder:  # we will store one channel since all images must be grayscale
        image = cv2.imread(os.path.join(path_to_current_emotion, file), cv2.IMREAD_GRAYSCALE)
        current_emotion_list.append(image)
      emotions_dict[emotion] = current_emotion_list  # saving list to dict
    return emotions_dict

  def LoadDatasetIntoRam(self) -> int:
    """Loads the dataset into RAM.

    This function checks if the dataset folder exists and is a directory.
    If it does, it loads the learning and testing sets into dictionaries.

    Args:
        None

    Returns:
        0 if successful, -1 otherwise.
    """
    # Checking dataset folder
    if not os.path.exists(self.dataset_path) or not os.path.isdir(self.dataset_path):
      print("Cannot find dataset folder")
      return -1

    # Loading learning set
    path_to_learning = os.path.join(self.dataset_path, self.forLearning)
    if os.path.exists(path_to_learning) and os.path.isdir(path_to_learning):
      self.learning_set_dict = self.ParseFolderWithEmotions(path_to_learning)

    # Loading testing set
    path_to_testing = os.path.join(self.dataset_path, self.forTesting)
    if os.path.exists(path_to_testing) and os.path.isdir(path_to_testing):
      self.testing_set_dict = self.ParseFolderWithEmotions(path_to_testing)

    return 0
