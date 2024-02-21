import unittest
import sys

sys.path.append("..")

import cv2
import os
import shutil
from shared import GetRelativePath, pretrained_face_detector
from ImageProcessing.face_detection import FaceDetector

# import pdb

sample_image_path = "sample1.jpg"
test_result_folder_name = "test_result/"

pfd_test_path = GetRelativePath("../" + pretrained_face_detector)
face_detector = FaceDetector(pfd_test_path)
sample_image = cv2.imread(sample_image_path)
# sample_image = cv2.resize(sample_image, (600,600))

faces = face_detector.DetectFaces(sample_image)
faceRect = faces[0].rect
coordinates_for_sample_image = face_detector.ConvertDlibToList(faceRect, sample_image)


class ImageProcessingTesting(unittest.TestCase):
  def test_DrawingFaceBox(self):
    image = face_detector.DrawFaceBox(sample_image, coordinates_for_sample_image)
    self.assertIsNotNone(image)
    cv2.imwrite(test_result_folder_name + "DrawingFaceBox.jpg", image)

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


if __name__ == "__main__":
  if os.path.exists(test_result_folder_name):
    shutil.rmtree(test_result_folder_name)
  os.mkdir(test_result_folder_name)
  unittest.main()
