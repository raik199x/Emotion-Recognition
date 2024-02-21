import dlib
import cv2
import numpy as np
from shared import drawing_color, drawing_thickness


class FaceDetector:
  def __init__(self, pretrained_face_detector_path: str):
    self.detector = dlib.cnn_face_detection_model_v1(pretrained_face_detector_path)
    self.image_improvement_level = 2

  def DetectFaces(self, image: np.array) -> dlib.mmod_rectangles:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return self.detector(gray, self.image_improvement_level)

  def ConvertDlibToList(
    self, face: dlib.mmod_rectangle, original_image: np.array
  ) -> list[tuple[int, int], tuple[int, int]]:
    # extract the starting and ending (x, y)-coordinates of the
    # bounding box
    startX = face.left()
    startY = face.top()
    endX = face.right()
    endY = face.bottom()
    # ensure the bounding box coordinates fall within the spatial
    # dimensions of the image
    startX = max(0, startX)
    startY = max(0, startY)
    endX = min(endX, original_image.shape[1])
    endY = min(endY, original_image.shape[0])

    face_coordinates = []
    face_coordinates.append((startX, startY))
    face_coordinates.append((endX, endY))
    return face_coordinates

  def DrawFaceBox(self, image: np.array, face: list[tuple[int, int], tuple[int, int]]) -> np.array:
    if len(face) != 2:
      print("face coordinates is messed up")  #! use logging system
      return None
    result_image = image.copy()
    upper_left_x, upper_left_y = face[0]
    down_left_x, down_left_y = face[1]

    cv2.rectangle(
      result_image, (upper_left_x, upper_left_y), (down_left_x, down_left_y), drawing_color, drawing_thickness
    )
    return result_image

  def CropFaceBox(self, image: np.array, face: list[tuple[int, int], tuple[int, int]]) -> np.array:
    if len(face) != 2:
      print("face coordinates is messed up")  #! use logging system
      return None
    result_image = image.copy()
    upper_left_x, upper_left_y = face[0]
    down_left_x, down_left_y = face[1]
    return result_image[upper_left_y:down_left_y, upper_left_x:down_left_x]
