import numpy as np
import cv2
import torch
from DeepLearning.settings import pytorch_device
from DeepLearning.dataset_parser import DatasetParser


class Connector:
  def __init__(self):
    self.Parser = DatasetParser("stub")  # Empty parser

  def is_grayscale(self, image: np.array):
    # Check the number of channels in the image
    return image.ndim == 2 or (image.ndim == 3 and image.shape[2] == 1)

  def ImageIntoTensor(self, original_image: np.array) -> torch.tensor:
    # Checking if image is already gray
    image = original_image.copy()
    if not self.is_grayscale(image):
      image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Now checking if image is suitable size
    height, width = image.shape[:2]
    if height != 48 or width != 48:
      image = cv2.resize(image, (48, 48))

    # Converting to tensor
    return torch.from_numpy(image).to(pytorch_device).to(torch.float32)

  def ClassificationResultIntoEmotion(self, class_result: torch.tensor) -> str:
    result_index = torch.argmax(class_result)
    for emotion in self.Parser.emotion_list:
      expect = self.Parser.emotion_expected_dict[emotion]
      if expect.index(max(expect)) == result_index:
        return emotion
    return "UNKNOWN"
