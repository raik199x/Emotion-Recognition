import unittest
import sys

sys.path.append("..")

import cv2
import os
import shutil
import torch
import numpy as np
from DeepLearning.model import EmotionClassificationModel
from DeepLearning.dataset_parser import DatasetParser
from shared import (
  GetRelativePath,
  pretrained_face_detector,
  pretrained_face_landmarks_predictor_model,
  pretrained_emotion_recognition_model,
)
from ImageProcessing.face_detection import FaceDetector
from ImageProcessing.facial_landmarks import FaceLandmarkPredictor

# import pdb # for debugging

# Constants
sample_image_path = "sample1.jpg"
test_result_folder_name = "test_result/"

# Pre-creating classes that we going to test
pfd_test_path = GetRelativePath("../" + pretrained_face_detector)
face_detector = FaceDetector(pfd_test_path, 2)

pflpm_test_path = GetRelativePath("../" + pretrained_face_landmarks_predictor_model)
face_landmark_predictor = FaceLandmarkPredictor(pflpm_test_path)

# Pre-detecting face (pretrained model does not requires testing :D)
sample_image = cv2.imread(sample_image_path)
sample_image = cv2.resize(sample_image, (400, 400))  # increasing image size since 48x48 is to small to see landmarks
faces = face_detector.DetectFaces(sample_image)
faceRect = faces[0].rect
coordinates_for_sample_image = face_detector.ConvertDlibToList(faceRect, sample_image)


class ImageProcessingTesting(unittest.TestCase):
  def test_DrawingFaceBox(self):
    image = face_detector.DrawFaceBox(sample_image, coordinates_for_sample_image)
    self.assertIsNotNone(image)
    cv2.imwrite(test_result_folder_name + "DrawingFaceBox.jpg", image)
    return image

  def test_CroppingFaceBox(self):
    image = face_detector.CropFaceBox(sample_image, coordinates_for_sample_image)
    self.assertIsNotNone(image)
    cv2.imwrite(test_result_folder_name + "CroppingFaceBox.jpg", image)

  def test_CroppingDrawingFaceBox(self):
    image = face_detector.DrawFaceBox(sample_image, coordinates_for_sample_image)
    self.assertIsNotNone(image)
    image = face_detector.CropFaceBox(image, coordinates_for_sample_image)
    self.assertIsNotNone(image)
    cv2.imwrite(test_result_folder_name + "CroppedDrawingFaceBox.jpg", image)

  def test_DetectingLandmarks(self):
    shape_landmarks = face_landmark_predictor.DetectLandmarks(sample_image, faceRect)
    coordinates_landmarks = face_landmark_predictor.ShapeToNp(shape_landmarks)
    self.assertEqual(len(coordinates_landmarks), 68)
    return coordinates_landmarks

  def test_DrawingLandmarks(self):
    cv2.imwrite(
      test_result_folder_name + "DrawingLandmarks.jpg",
      face_landmark_predictor.DrawLandmarks(sample_image, self.test_DetectingLandmarks()),
    )

  def test_DrawingBoxPlacingLandmarks(self):
    image = self.test_DrawingFaceBox()
    coordinates_landmarks = self.test_DetectingLandmarks()
    result_image = face_detector.DrawFaceBox(image, coordinates_for_sample_image)
    result_image = face_landmark_predictor.DrawLandmarks(result_image, coordinates_landmarks)
    cv2.imwrite(test_result_folder_name + "DrawingBoxLandmark.jpg", result_image)


class ModelTesting(unittest.TestCase):
  def test_TriggeringTestingEpoch(self):
    # Loading module
    emotion_classification_model = EmotionClassificationModel()
    if os.path.exists("../" + pretrained_emotion_recognition_model):  # if exists better using our model
      emotion_classification_model.LoadModel("../" + pretrained_emotion_recognition_model)

    # Getting value for testing
    parser = DatasetParser("dataset")
    self.assertEqual(parser.LoadDatasetIntoRam(), 0)

    emotion = parser.angry
    test_value = parser.learning_set_dict[emotion][0]  # taking first image
    tensor = torch.from_numpy(test_value).to(torch.float32)

    expected_tensor = torch.from_numpy(np.array(parser.emotion_expected_dict[emotion])).to(torch.float32)

    # Getting testing result
    fun_result = emotion_classification_model.TestingEpoch(tensor, expected_tensor)
    print(fun_result)

  def test_OutputStateDict(self):
    # Loading module
    emotion_classification_model = EmotionClassificationModel()
    if not os.path.exists("../" + pretrained_emotion_recognition_model):
      return
    emotion_classification_model.LoadModel("../" + pretrained_emotion_recognition_model)
    print(emotion_classification_model.state_dict())


if __name__ == "__main__":
  if os.path.exists(test_result_folder_name):
    shutil.rmtree(test_result_folder_name)
  os.mkdir(test_result_folder_name)
  unittest.main()
