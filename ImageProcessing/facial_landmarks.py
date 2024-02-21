import numpy as np
import dlib
import cv2


class FaceLandmarkPredictor:
  def __init__(self, face_landmarks_predictor_file_path):
    self.predictor = dlib.shape_predictor(face_landmarks_predictor_file_path)

  def ShapeToNp(self, shape: dlib.full_object_detection, dtype="int") -> list[[int, int], ...]:
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)
    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
      coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords  # return the list of (x, y)-coordinates

  def DrawLandmarks(self, original_image: np.array, coordinates_landmarks: list[[int, int], ...]) -> np.array:
    result_image = original_image.copy()
    for x, y in coordinates_landmarks:
      cv2.circle(result_image, (x, y), 1, (0, 0, 255), -1)
    return result_image

  def DetectLandmarks(self, image: np.array, face: dlib.mmod_rectangle) -> dlib.full_object_detection:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return self.predictor(gray, face)
