from PySide6.QtCore import QRunnable, Slot
from DeepLearning.settings import pytorch_device
from DeepLearning.dataset_parser import DatasetParser
import torch
import numpy as np
from shared import GetRelativePath, pretrained_emotion_recognition_model

PretrainedModelRelativePath = GetRelativePath(pretrained_emotion_recognition_model)


class LearningWorker(QRunnable):
  """
  Worker thread that runs learning function
  """

  def __init__(self, MainWindowClass, ParentClass):
    super(LearningWorker, self).__init__()
    self.MainWindowClass = MainWindowClass
    self.ParentClass = ParentClass

  def UpdateAndSave(self):
    self.ParentClass.label_current_epoch.setText(str(self.ParentClass.current_epoch))
    self.ParentClass.label_current_emotion.setText(self.ParentClass.current_emotion)
    self.ParentClass.label_full_dataset_iteration.setText(str(self.ParentClass.full_dataset_iteration))
    self.MainWindowClass.emotion_classification_model.BackupModel("", PretrainedModelRelativePath)

  @Slot()
  def run(self):
    parser = DatasetParser()
    while self.MainWindowClass.is_model_learning:
      emotion_generators = list()
      for emotion in parser.emotion_list:  # Filling emotion generator list
        emotion_generators.append(parser.EmotionNpPointGenerator(parser.forLearning, emotion))

      for num, emotion in enumerate(emotion_generators):
        self.ParentClass.current_emotion = parser.emotion_list[num]
        expect = (
          torch.from_numpy(np.array(parser.emotion_expected_dict[parser.emotion_list[num]]))
          .to(torch.float32)
          .to(pytorch_device)
        )
        for train_value in emotion:
          # Sending training data
          tensor = torch.from_numpy(train_value).to(pytorch_device).to(torch.float32)
          self.MainWindowClass.emotion_classification_model.TrainEpoch(tensor, expect)

          if not self.MainWindowClass.is_model_learning:
            return

          self.ParentClass.current_epoch = self.ParentClass.current_epoch + 1
          # Updating stats and saving model
          if self.ParentClass.current_epoch % self.ParentClass.update_after_num_epochs == 0:
            self.UpdateAndSave()

      self.ParentClass.full_dataset_iteration = self.ParentClass.full_dataset_iteration + 1

    # Exiting thread
    self.UpdateAndSave()
