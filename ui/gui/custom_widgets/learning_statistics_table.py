from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QTableView
from DeepLearning.dataset_parser import DatasetParser


class LearningStatisticsTable(QTableView):
  def __init__(self, parser: DatasetParser):
    super().__init__()
    self.model = QStandardItemModel()
    self.setModel(self.model)
    self.setSortingEnabled(True)

    self.column_names = ["Emotion name", "Guessed right", "Total amount", "Average loss"]
    self.model.setColumnCount(len(self.column_names))
    self.model.setHorizontalHeaderLabels(self.column_names)

    self.amount_of_emotions = len(parser.emotion_list)
    self.model.setRowCount(self.amount_of_emotions)
    for num, emotion in enumerate(parser.emotion_list):
      self.model.setItem(num, 0, QStandardItem(emotion))
      self.model.setItem(num, 1, QStandardItem("no iterations"))
      content = str(len(parser.testing_set_dict[emotion])) if parser.isParserLoaded else "0"
      self.model.setItem(num, 2, QStandardItem(content))
      self.model.setItem(num, 3, QStandardItem("no iterations"))

    self.setShowGrid(True)

  def set_data(self, guessed_right: list[int, ...], average_values: list[float, ...]):
    for num in range(0, self.amount_of_emotions):
      self.model.setItem(num, 1, QStandardItem(str(guessed_right[num])))
      self.model.setItem(num, 3, QStandardItem(str(round(average_values[num], 5))))
