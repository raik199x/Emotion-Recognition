from PySide6.QtCore import QRunnable, Slot, Signal, QObject
from DeepLearning.settings import pytorch_device
from DeepLearning.dataset_parser import DatasetParser
import torch
import numpy as np
from shared import GetRelativePath, pretrained_emotion_recognition_model
from connector import Connector

# from random import shuffle

PretrainedModelRelativePath = GetRelativePath(pretrained_emotion_recognition_model)


class LearningWorkerSignals(QObject):  # Creating signal so we can send data from testing loop
  redo_plots_signal = Signal(list, list)
  update_epoch_stats_signal = Signal(int, str, list, list)
  update_emotion_classification_result_signal = Signal(list, list)


class LearningWorker(QRunnable):
  """
  Worker thread that runs learning function
  """

  def __init__(self, MainWindowClass, update_after_num_epochs: int, parser: DatasetParser):
    super(LearningWorker, self).__init__()
    self.MainWindowClass = MainWindowClass
    # self.update_after_num_epochs = update_after_num_epochs
    self.signals = LearningWorkerSignals()
    self.parser = parser
    self.connector = Connector()
    self.update_cycle = update_after_num_epochs

    self.current_epoch = int()
    self.last_triggered_emotion = str

  def UpdateAndSave(self, expected_list: list[int, ...], tensor_result: [float, ...]):
    tensor_result = [round(num, 5) for num in tensor_result]
    self.signals.update_epoch_stats_signal.emit(
      self.current_epoch, self.last_triggered_emotion, expected_list, tensor_result
    )
    self.MainWindowClass.emotion_classification_model.BackupModel("", PretrainedModelRelativePath)

  def TestingModel(self, parser: DatasetParser) -> list:
    # Stats collector
    accuracy_results = list()
    loss_fn_results = list()
    emotion_average_loss = list()
    emotions_classification_result = list()

    for emotion in parser.emotion_list:
      expect = torch.from_numpy(np.array(parser.emotion_expected_dict[emotion])).to(torch.float32).to(pytorch_device)
      predicted_right = 0
      current_loss_coefficients = list()  # Storing all loss coefficient for current emotion
      for test_value in parser.testing_set_dict[emotion]:
        # Sending test data
        tensor = self.connector.ImageIntoTensor(test_value)

        fun_result = self.MainWindowClass.emotion_classification_model.TestingEpoch(tensor, expect)

        # Collecting stats
        accuracy_results.append(fun_result["Accuracy"])
        loss_fn_results.append(fun_result["Loss"])
        current_loss_coefficients.append(fun_result["Loss"])
        predicted_right = predicted_right + 1 if fun_result["IsPredictedRight"] else 0

        if not self.MainWindowClass.is_model_learning:  # If user pressed stop button
          return "INTERRUPTED"  # TODO remove hardcode

      # Calculating average loss and saving results
      emotion_average_loss.append(sum(current_loss_coefficients) / len(current_loss_coefficients))
      emotions_classification_result.append(predicted_right)

    # Emitting signal and sending data to main thread
    self.signals.redo_plots_signal.emit(loss_fn_results, accuracy_results)
    self.signals.update_emotion_classification_result_signal.emit(emotions_classification_result, emotion_average_loss)
    return emotion_average_loss

  def LearningModel(self, parser: DatasetParser, emotion_index: int):
    self.last_triggered_emotion = parser.emotion_list[emotion_index]

    # One image at a time
    expect_list = parser.emotion_expected_dict[self.last_triggered_emotion]
    expect_tensor = torch.from_numpy(np.array(expect_list)).to(torch.float32).to(pytorch_device)
    if len(parser.learning_set_dict[self.last_triggered_emotion]) == 0:
      parser.ReloadEmotion(parser.forLearning, self.last_triggered_emotion)
    train_value = parser.learning_set_dict[self.last_triggered_emotion][-1]
    parser.learning_set_dict[self.last_triggered_emotion].pop()
    tensor = self.connector.ImageIntoTensor(train_value)
    result_tensor = self.MainWindowClass.emotion_classification_model.TrainEpoch(tensor, expect_tensor)

    # value_expected_list = list()
    # for emotion in parser.emotion_list:
    #   for test_value in parser.learning_set_dict[emotion]:
    #     value_expected_list.append([test_value, parser.emotion_expected_dict[emotion]])

    # shuffle(value_expected_list)
    # for value_expected in value_expected_list:
    #   expect_list = value_expected[1]
    #   expect_tensor = torch.from_numpy(np.array(expect_list)).to(torch.float32).to(pytorch_device)
    #   tensor = self.connector.ImageIntoTensor(value_expected[0])
    #   result_tensor = self.MainWindowClass.emotion_classification_model.TrainEpoch(tensor, expect_tensor)

    # Updating and sending results
    self.current_epoch = self.current_epoch + 1
    self.UpdateAndSave(expect_list, result_tensor.tolist())

  @Slot()
  def run(self):
    while self.MainWindowClass.is_model_learning:
      emotions_average_loss = self.TestingModel(self.parser)
      if emotions_average_loss == "INTERRUPTED":  # TODO: REMOVE HARDCODE
        break
      # Finding the worst identified emotion and telling model to learn it
      self.LearningModel(self.parser, emotions_average_loss.index(max(emotions_average_loss)))
