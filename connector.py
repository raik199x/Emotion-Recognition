import numpy as np
import cv2
import torch
from DeepLearning.settings import pytorch_device
from DeepLearning.dataset_parser import DatasetParser


class Connector:
  def __init__(self):
    self.Parser = DatasetParser("stub")  # Empty parser

  def IsGrayscale(self, image: np.array) -> bool:
    # Check the number of channels in the image
    return image.ndim == 2 or (image.ndim == 3 and image.shape[2] == 1)

  def ImageIntoTensor(self, original_image: np.array) -> torch.tensor:
    # Checking if image is already gray
    image = original_image.copy()
    if not self.IsGrayscale(image):
      image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Now checking if image is suitable size
    height, width = image.shape[:2]
    if height != 48 or width != 48:
      image = cv2.resize(image, (48, 48))

    image = np.divide(image, 1000)  # Making all values between 0 and 1

    # Converting to tensor
    return torch.from_numpy(image).to(pytorch_device).to(torch.float32).flatten()

  def ClassificationResultIntoEmotion(self, class_result: torch.tensor) -> str:
    result_index = torch.argmax(class_result)
    for emotion in self.Parser.emotion_list:
      expect = self.Parser.emotion_expected_dict[emotion]
      if expect.index(max(expect)) == result_index:
        return emotion
    raise IndexError("Tensor list is bigger than expected list, so could not find emotion")
