from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from ui.gui.custom_widgets.dark_style_button import DarkStyleButton
from shared import icon_size, assets_folder_path


class AbstractStorageWidget(QWidget):
  def __init__(self, icon_path: str, storage_class):
    super().__init__()
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)
    self.setFixedHeight(85)

    container_widget = QFrame()
    container_widget.setStyleSheet("background-color: #272727; border-radius: 10px;")
    basic_info = QHBoxLayout(container_widget)

    cloud_storage_icon = QLabel()
    cloud_storage_icon.setPixmap(QPixmap(icon_path).scaled(icon_size))
    cloud_storage_icon.setAlignment(Qt.AlignCenter)

    overview_layout = QVBoxLayout()
    self.label_status = QLabel("Nothing to do now")
    self.label_status.setAlignment(Qt.AlignRight)

    buttons_layout = QHBoxLayout()  # start buttons layout

    button_push = DarkStyleButton("Push")
    button_push.setToolTip("Pushes folder to the cloud")
    button_push.clicked.connect(self.pushPressed)

    button_pull = DarkStyleButton("Pull")
    button_pull.setToolTip("Pulls folder from the cloud")
    button_pull.clicked.connect(self.pullPressed)

    buttons_layout.addWidget(button_push)
    buttons_layout.addWidget(button_pull)  # end buttons layout

    overview_layout.addWidget(self.label_status)
    overview_layout.addLayout(buttons_layout)

    self.current_status_icon = QLabel()
    self.current_status_icon.setPixmap(QPixmap(assets_folder_path + "information.png").scaled(icon_size))  #! IMPLEMENT
    self.current_status_icon.setAlignment(Qt.AlignCenter)

    basic_info.addWidget(cloud_storage_icon)
    basic_info.addLayout(overview_layout)
    basic_info.addWidget(self.current_status_icon)

    main_layout.addWidget(container_widget)

    self.cloud_storage = storage_class

  def pullPressed(self):
    print("Button pull pressed")

  def pushPressed(self):
    print("Button push pressed")
