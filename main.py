from torch import __version__ as pytorch_version
import torch
from DeepLearning import dataset_parser, model, settings
import os
import numpy as np
import shared
import signal

global every_n_check_create_backup
every_n_check_create_backup = 10000
global continue_infinite_loop
continue_infinite_loop = True

emotion_recognition_model = model.EmotionClassificationModel().to(settings.pytorch_device)
if os.path.exists(shared.pretrained_emotion_recognition_model):
  print("reading backup")
  emotion_recognition_model.LoadModel(shared.pretrained_emotion_recognition_model)


def signal_handler(sig, frame):
  print("Stopping infinite loop")
  global continue_infinite_loop
  continue_infinite_loop = False


def EpochBasedTrainLoop(epoch: int):
  pass


def InfiniteTrainLoop():
  signal.signal(signal.SIGINT, signal_handler)  # redefine signal
  parser = dataset_parser.DatasetParser()
  emotion_generators = list()

  count = 0
  global continue_infinite_loop
  while continue_infinite_loop:
    for emotion in parser.emotion_list:
      emotion_generators.append(parser.EmotionNpPointGenerator(parser.forLearning, emotion))
    for emotion in emotion_generators:
      expect = (
        torch.from_numpy(np.array(parser.emotion_expected_dict[parser.angry]))
        .to(torch.float32)
        .to(settings.pytorch_device)
      )
      for train_value in emotion:
        tensor = torch.from_numpy(train_value).to(settings.pytorch_device).to(torch.float32)
        emotion_recognition_model.TrainEpoch(tensor, expect)

        if not continue_infinite_loop:
          exit(1)

        # Backup module
        count = count + 1
        if count == every_n_check_create_backup:
          count = 0
          emotion_recognition_model.BackupModel(shared.data_folder, "emotion_recognition_model.pt")
          print("model created backup")


if __name__ == "__main__":
  print(pytorch_version)
  print(settings.pytorch_device)

  InfiniteTrainLoop()
