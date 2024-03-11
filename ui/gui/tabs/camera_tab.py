import cv2
import connector
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QCheckBox
from ui.gui.tabs.abstract_tab import AbstractTabWidget
from ImageProcessing.face_detection import FaceDetector
from shared import pretrained_face_detector


class CameraTab(AbstractTabWidget):
  def __init__(self, ParentClass, tab_name):
    super().__init__(ParentClass, tab_name)

    self.connector = connector.Connector()
    self.FaceDetector = FaceDetector(pretrained_face_detector, 0)

    # Create the layout and add the image label to it
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)

    self.checkbox_display_faceBox = QCheckBox("Display face box")
    self.checkbox_display_faceBox.setEnabled(True)
    main_layout.addWidget(self.checkbox_display_faceBox)

    self.checkbox_display_emotion = QCheckBox("Display Emotion")
    self.checkbox_display_emotion.setEnabled(True)
    main_layout.addWidget(self.checkbox_display_emotion)

    # Create the QLabel to display the video feed
    self.image_label = QLabel(self)
    self.image_label.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(self.image_label)

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

    cropped_images = list()
    coordinates = list()

    dlib_faces = self.FaceDetector.DetectFaces(frame)
    for dlib_face in dlib_faces:
      dlib_face = dlib_face.rect
      coordinates.append(self.FaceDetector.ConvertDlibToList(dlib_face, frame))
      cropped_images.append(self.FaceDetector.CropFaceBox(frame, coordinates[-1]))
      if self.checkbox_display_faceBox.isChecked():
        frame = self.FaceDetector.DrawFaceBox(frame, coordinates[-1])

    if self.checkbox_display_emotion.isChecked():
      for num, face in enumerate(cropped_images):
        tensor = self.connector.ImageIntoTensor(face)
        class_result = self.ParentClass.emotion_classification_model(tensor)
        emotion_name = self.connector.ClassificationResultIntoEmotion(class_result)
        # cv2.putText(image_with_text, text, position, font, font_scale, color, thickness)
        cv2.putText(frame, emotion_name, coordinates[num][0], cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

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
