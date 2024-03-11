import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout
from ui.gui.tabs.abstract_tab import AbstractTabWidget
from ImageProcessing.face_detection import FaceDetector
from shared import pretrained_face_detector


class CameraTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)

    self.FaceDetector = FaceDetector(pretrained_face_detector, 0)
    # Create the QLabel to display the video feed
    self.image_label = QLabel(self)
    self.image_label.setAlignment(Qt.AlignCenter)

    # Create the layout and add the image label to it
    layout = QVBoxLayout()
    layout.addWidget(self.image_label)

    # Set the layout for the widget
    self.setLayout(layout)

    # Create the timer for updating the video feed
    self.timer = QTimer(self)
    self.timer.timeout.connect(self.update_frame)
    self.timer.start(30)  # Update the frame every 30 milliseconds

    # Open the camera using OpenCV
    self.capture = cv2.VideoCapture(0)  # 0 represents the default camera

  def update_frame(self):
    # Read the frame from the camera
    ret, frame = self.capture.read()
    if not ret:
      return

    #! ADDING CHECKBOX FOR THIS
    dlib_faces = self.FaceDetector.DetectFaces(frame)
    cropped_images = list()
    for dlib_face in dlib_faces:
      dlib_face = dlib_face.rect
      coordinates = self.FaceDetector.ConvertDlibToList(dlib_face, frame)
      cropped_images.append(self.FaceDetector.CropFaceBox(frame, coordinates))
      frame = self.FaceDetector.DrawFaceBox(frame, coordinates)

    #! AND FOR THIS
    # for face in cropped_images:

    # Convert the frame to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Create a QImage from the frame data
    image = QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888)

    # Create a QPixmap from the QImage
    pixmap = QPixmap.fromImage(image)

    # Scale the pixmap to fit the label size
    # scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)

    # Set the pixmap on the label to display the video feed
    self.image_label.setPixmap(pixmap)
