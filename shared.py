from sys import argv
from os import path
from PySide6.QtCore import QSize

# Paths
assets_folder_path = "assets/"
data_folder_path = "emotion_recognition_data/"
dataset_folder_path = data_folder_path + "dataset/"
pretrained_face_landmarks_predictor_model = data_folder_path + "shape_predictor_68_face_landmarks.dat"
pretrained_face_detector = data_folder_path + "mmod_human_face_detector.dat"
pretrained_emotion_recognition_model = data_folder_path + "emotion_recognition_model.pt"


def GetRelativePath(var):
  relative_path = argv[0]
  if relative_path.rfind("/") == -1:
    return var
  relative_path = relative_path[: relative_path.rfind("/")]
  return path.join(relative_path, var)


# Image drawing settings
drawing_color = (0, 255, 0)  # Default green
drawing_thickness = 1

# Gui
icon_size = QSize(40, 40)