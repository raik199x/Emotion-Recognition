from torch import __version__ as pytorch_version
from DeepLearning import dataset_parser, model, settings
import os
import numpy as np
import shared

if __name__ == "__main__":
  print(pytorch_version)
  print(settings.pytorch_device)

  parser = dataset_parser.DatasetParser()
  generator = parser.EmotionNpPointGenerator(parser.forLearning, parser.angry)
  expect = np.array([1, 0, 0, 0, 0, 0, 0])
  values = next(generator)

  emotion_recognition_model = model.EmotionClassificationModel().to(settings.pytorch_device)
  if os.path.exists(shared.pretrained_emotion_recognition_model):
    emotion_recognition_model.LoadModel(shared.pretrained_emotion_recognition_model)
    print(emotion_recognition_model.state_dict())

  emotion_recognition_model.TrainEpoch(values, expect)

  emotion_recognition_model.BackupModel(shared.data_folder, "emotion_recognition_model.pt")
  print(emotion_recognition_model.state_dict())
