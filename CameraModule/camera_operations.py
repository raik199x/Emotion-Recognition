import cv2


class CameraOperations:
  def __init__(self):
    self.camera = cv2.VideoCapture(0)

  def TakePhoto(self):
    ret, img = self.camera.read()[1]
    return img
