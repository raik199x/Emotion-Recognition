import unittest
from ImageProcessing.facial_landmarks import FaceManipulations
from ImageProcessing.settings import face_landmarks_predictor
import os

import dlib

import cv2


class ImageProcessingTesting(unittest.TestCase):
  # def test_placingFaceLandmarks(self):
  #   folder_for_result = "face_landmarks/"
  #   test_files_folder = "dataset/test/angry/"
  #   testing_class = FaceManipulations(face_landmarks_predictor)

  #   # managing folder
  #   if os.path.exists(folder_for_result):
  #     os.rmdir(folder_for_result)
  #   os.mkdir(folder_for_result)

  #   files = os.listdir(test_files_folder)
  #   for num, file in enumerate(files):
  #     file = test_files_folder + file
  #     img = testing_class.SetFacialLandmarks(file)
  #     imwrite(folder_for_result + str(num) + ".jpg", img)

  def test_faceDetection(self):
    test_files_folder = "dataset/test/angry/"
    testing_class = FaceManipulations("ImageProcessing/" + face_landmarks_predictor)
    files = os.listdir(test_files_folder)

    total = len(files)
    found = 0
    for num, file in enumerate(files):
      file = test_files_folder + file
      rectangles = testing_class.DetectFace(file)

      found = found + len(rectangles)
      break

    print("Stat: " + str(found) + "/" + str(total))

  def test_faceDetectionV1(self):
    """
    detector stats based on kaggle dataset angry faces
    image resolution is 48x48, grayscale, cpu
    _____________________________________________________________________
    |Image improvement level | identified faces / all faces  | time (sec)|
    |1                       | 806 / 956                     | 45        |
    |2                       | 893 / 956                     | 174       |
    |3                       | 883 / 956                     | 796       |
    |4                       | 883 / 956                     | 3490      |
    |5                       | ?   / 956                     | Eternity  |
    |____________________________________________________________________|
    """
    test_files_folder = "dataset/test/angry/"
    detector = dlib.cnn_face_detection_model_v1("ImageProcessing/" + "mmod_human_face_detector.dat")
    files = os.listdir(test_files_folder)

    total = len(files)
    found = 0
    for num, file in enumerate(files):
      file = test_files_folder + file
      image = cv2.imread(file)
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      result = detector(gray, 5)

      found = found + len(result)

    print("Stat: " + str(found) + "/" + str(total))
