import unittest
import sys

sys.path.append("..")

import cv2
import os
import shutil
from shared import GetRelativePath, pretrained_face_detector, pretrained_face_landmarks_predictor_model
from ImageProcessing.face_detection import FaceDetector
from ImageProcessing.facial_landmarks import FaceLandmarkPredictor

# import pdb # for debugging

# Constants
sample_image_path = "sample1.jpg"
test_result_folder_name = "test_result/"

# Pre-creating classes that we going to test
pfd_test_path = GetRelativePath("../" + pretrained_face_detector)
face_detector = FaceDetector(pfd_test_path)

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


if __name__ == "__main__":
  if os.path.exists(test_result_folder_name):
    shutil.rmtree(test_result_folder_name)
  os.mkdir(test_result_folder_name)
  unittest.main()
