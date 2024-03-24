import os
from ImageProcessing.face_detection import FaceDetector
import cv2

# Preparing data
face_detector = FaceDetector("../emotion_recognition_data/mmod_human_face_detector.dat", 2)
path_to_dataset = "../emotion_recognition_data/dataset/test/"
list_of_folder = ["angry/", "disgust/", "fear/", "happy/", "neutral/", "sad/", "surprise/"]

# Performing script
for folder in list_of_folder:
  print("-----------------------------")
  print(f"Current folder: {folder}.")
  files_in_folder = os.listdir(path_to_dataset + folder)
  # print(f"Total files: {len(files_in_folder)}")
  count = 0
  for num, file in enumerate(files_in_folder):
    image = cv2.imread(path_to_dataset + folder + file)
    image = cv2.resize(image, (200, 200))
    faces = face_detector.DetectFaces(image)
    if len(faces) != 1:
      count = count + 1
      os.remove(path_to_dataset + folder + file)
    if num % 100 == 0:
      print(f"Analyzed {str(num)} files")

  print(f"Analyze result (deleted): {str(count)}/{str(len(files_in_folder))}")
  print("--------------------------------")
