# from imutils import face_utils
import numpy as np
import dlib
import cv2
# from ImageProcessing.settings import face_landmarks_predictor


class FaceLandmarkPrediction:
  def __init__(self, face_landmarks_predictor_file_path):
    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    self.detector = dlib.get_frontal_face_detector()
    self.predictor = dlib.shape_predictor(face_landmarks_predictor_file_path)

  def ShapeToNp(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)
    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
      coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords  # return the list of (x, y)-coordinates

  def DrawLandmarks():
    pass

  def DetectLandmarks():
    pass

  # def SetFacialLandmarks(self, path_to_image):
  #   # load the input image, resize it, and convert it to grayscale
  #   image = cv2.imread(path_to_image)
  #   image = cv2.resize(image, (500, 500))
  #   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  #   # detect faces in the grayscale image
  #   rects = self.detector(gray, 1)  # can work with colored images as well

  #   # loop over the face detections
  #   for i, rect in enumerate(rects):
  #     # determine the facial landmarks for the face region, then
  #     # convert the facial landmark (x, y)-coordinates to a NumPy
  #     # array
  #     shape = self.predictor(gray, rect)
  #     shape = self.shape_to_np(shape)
  #     # convert dlib's rectangle to a OpenCV-style bounding box
  #     # [i.e., (x, y, w, h)], then draw the face bounding box
  #     (x, y, w, h) = face_utils.rect_to_bb(rect)
  #     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
  #     # show the face number
  #     cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
  #     # loop over the (x, y)-coordinates for the facial landmarks
  #     # and draw them on the image
  #     for x, y in shape:
  #       cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

  #   return image
