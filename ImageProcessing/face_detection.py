import dlib
import cv2
import shared


class FaceDetector:
  def __init__(self, pretrained_face_detector_path):
    self.detector = dlib.cnn_face_detection_model_v1(shared.GetRelativePath(shared.face_detector))
    self.image_improvement_level = 2

  def DetectFaces(self, image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return self.detector(gray, self.image_improvement_level)

  def DrawFaceBox(self, image):
    pass
