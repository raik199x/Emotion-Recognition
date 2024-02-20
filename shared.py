from sys import argv
from os import path

face_landmarks_predictor = "data/shape_predictor_68_face_landmarks.dat"
face_detector = "data/mmod_human_face_detector.dat"


def GetRelativePath(var):
  return path.join(argv[0], var)
