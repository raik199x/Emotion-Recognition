from PySide6.QtCore import QRunnable, Slot, Signal, QObject
from DeepLearning.settings import pytorch_device
from DeepLearning.dataset_parser import DatasetParser
import torch
import numpy as np
from shared import GetRelativePath, pretrained_emotion_recognition_model

PretrainedModelRelativePath = GetRelativePath(pretrained_emotion_recognition_model)


class LearningWorkerSignals(QObject):  # Creating signal so we can send data from testing loop
  redo_plots_signal = Signal(list, list)
  update_epoch_stats_signal = Signal(int, str, int)
  update_emotion_classification_result_signal = Signal(list)


class LearningWorker(QRunnable):
  """
  Worker thread that runs learning function
  """

  def __init__(self, MainWindowClass, update_after_num_epochs):
    super(LearningWorker, self).__init__()
    self.MainWindowClass = MainWindowClass
    self.update_after_num_epochs = update_after_num_epochs
    self.signals = LearningWorkerSignals()

    self.current_epoch = int()
    self.current_emotion = str
    self.full_dataset_iteration = int()

  def UpdateAndSave(self):
    self.signals.update_epoch_stats_signal.emit(self.current_epoch, self.current_emotion, self.full_dataset_iteration)
    self.MainWindowClass.emotion_classification_model.BackupModel("", PretrainedModelRelativePath)

  def TestingModel(self, parser):
    emotion_generators = list()

    # Stats collector
    accuracy_results = list()
    loss_fn_results = list()
    emotions_classification_result = list()
    for _ in range(0, len(parser.emotion_list)):
      emotions_classification_result.append(0)

    for emotion in parser.emotion_list:  # Filling emotion generator list
      emotion_generators.append(parser.EmotionNpPointGenerator(parser.forTesting, emotion))

    for num, emotion in enumerate(emotion_generators):
      expect = (
        torch.from_numpy(np.array(parser.emotion_expected_dict[parser.emotion_list[num]]))
        .to(torch.float32)
        .to(pytorch_device)
      )
      predicted_right = 0
      for test_value in emotion:
        # Sending test data
        tensor = torch.from_numpy(test_value).to(pytorch_device).to(torch.float32)

        fun_result = self.MainWindowClass.emotion_classification_model.TestingEpoch(tensor, expect)
        # Collecting stats
        accuracy_results.append(fun_result["Accuracy"])
        loss_fn_results.append(fun_result["Loss"])
        predicted_right = predicted_right + 1 if fun_result["IsPredictedRight"] else 0

        if not self.MainWindowClass.is_model_learning:
          return

      emotions_classification_result[num] = predicted_right

    # Emitting signal and sending data to main thread
    self.signals.redo_plots_signal.emit(loss_fn_results, accuracy_results)
    self.signals.update_emotion_classification_result_signal.emit(emotions_classification_result)

  def LearningModel(self, parser):
    emotion_generators = list()
    for emotion in parser.emotion_list:  # Filling emotion generator list
      emotion_generators.append(parser.EmotionNpPointGenerator(parser.forLearning, emotion))

    for num, emotion in enumerate(emotion_generators):
      self.current_emotion = parser.emotion_list[num]
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

        self.current_epoch = self.current_epoch + 1
        # Updating stats and saving model
        if self.current_epoch % self.update_after_num_epochs == 0:
          self.UpdateAndSave()
          self.TestingModel(parser)

    self.full_dataset_iteration = self.full_dataset_iteration + 1

  @Slot()
  def run(self):
    parser = DatasetParser()
    while self.MainWindowClass.is_model_learning:
      self.LearningModel(parser)  # Testing triggers inside
    # Exiting thread
    self.UpdateAndSave()
