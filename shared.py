from sys import argv
from os import path

face_landmarks_predictor = "data/shape_predictor_68_face_landmarks.dat"
pretrained_face_detector = "data/mmod_human_face_detector.dat"


def GetRelativePath(var):
  relative_path = argv[0]
  if relative_path.rfind("/") == -1:
    return var
  relative_path = relative_path[: relative_path.rfind("/")]
  return path.join(relative_path, var)


# Image drawing settings
drawing_color = (0, 255, 0)  # Default green
drawing_thickness = 2
