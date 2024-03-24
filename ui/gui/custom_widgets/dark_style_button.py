from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt


class DarkStyleButton(QPushButton):
  def __init__(self, text, parent=None):
    super().__init__(text, parent)
    self.setStyleSheet("border: none; padding: 5px;")
    # Background color of button
    self.active_button_color = QColor("#303030")
    self.disabled_button_color = QColor("#464646")
    self.hovered_button_color = QColor("#000")
    self.clicked_button_color = QColor("#464646")
    # Flags
    self.isButtonClicked = False

  def redrawBackgroundColor(self, painter, bg_color):
    # Draw the rounded background
    rounded_rect = self.rect().adjusted(1, 1, -1, -1)
    painter.setBrush(bg_color)
    painter.setPen(QPen(QColor("#FFF"), 1))
    painter.drawRoundedRect(rounded_rect, 10, 10)

  def redrawText(self, painter, align=Qt.AlignCenter, text="None"):
    # Draw the text
    painter.setPen(QColor("#FFF"))
    painter.drawText(self.rect(), align, text)

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)

    # Determine the background color based on the hover state
    if self.isButtonClicked:
      bg_color = self.disabled_button_color
    elif self.underMouse() and self.isEnabled():
      bg_color = self.hovered_button_color
    elif not self.isEnabled():
      bg_color = self.disabled_button_color
    else:
      bg_color = self.active_button_color

    # Draw the rounded background
    self.redrawBackgroundColor(painter, bg_color)
    # Draw the text
    self.redrawText(painter, Qt.AlignCenter, self.text())

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.isButtonClicked = True
      self.repaint()
      super().mousePressEvent(event)

  def mouseReleaseEvent(self, event):
    if event.button() == Qt.LeftButton:
      self.isButtonClicked = False
      self.repaint()
      super().mouseReleaseEvent(event)
