from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QComboBox, QFormLayout, QLineEdit, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from ui.gui.custom_widgets.dark_style_button import DarkStyleButton
from CloudStorages.mega import MegaCloud
import config_parser


class AddStorageDialog(QDialog):
  def __init__(self):
    super().__init__()
    self.isCancelExit = True  # flag
    self.regular_expression_no_spaces = QRegularExpressionValidator(QRegularExpression(r"\S+"))
    self.setWindowTitle("Adding storage")
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)

    storage_provider_layout = QFormLayout()
    self.combo_box = QComboBox()
    self.combo_box.addItem("Mega.nz")
    self.combo_box.addItem("Yandex.disk")
    self.combo_box.currentIndexChanged.connect(self.comboBoxItemChanged)

    combo_box_name = QLabel("Choose storage provider: ")
    storage_provider_layout.addRow(combo_box_name, self.combo_box)
    main_layout.addLayout(storage_provider_layout)
    # end of storage_provider_layout

    self.credentials_widget = self.getCredentialsWidget(self.combo_box.currentText())
    main_layout.addWidget(self.credentials_widget)

    self.label_status = QLabel("Nothing bad so far")
    self.label_status.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(self.label_status)

    button_layout = QHBoxLayout()
    button_cancel = DarkStyleButton("Cancel")
    button_cancel.clicked.connect(self.close)

    button_confirm = DarkStyleButton("Confirm")
    button_confirm.clicked.connect(self.confirmClicked)

    button_layout.addWidget(button_cancel)
    button_layout.addWidget(button_confirm)
    main_layout.addLayout(button_layout)

  def confirmClicked(self) -> None:
    if len(self.line_edit_storage_name.text()) == 0:
      self.label_status.setText("Storage name is empty!")
      self.label_status.setStyleSheet("color: yellow;")
      return
    saving_credentials = config_parser.ProjectConfig()

    if self.combo_box.currentText() == "Mega.nz":
      if len(self.line_edit_email_input.text()) == 0 or len(self.line_edit_password_input.text()) == 0:
        self.label_status.setText("Email or password are empty")
        self.label_status.setStyleSheet("color: yellow;")
        return

      test = MegaCloud()
      result = test.loginViaCredentials(self.line_edit_email_input.text(), self.line_edit_password_input.text())
      if not result == test.success_code:
        self.label_status.setText(str(result))
        self.label_status.setStyleSheet("color: yellow;")
        return

      result = saving_credentials.addMegaStorage(
        self.line_edit_storage_name.text(), self.line_edit_email_input.text(), self.line_edit_password_input.text()
      )
      if not result == saving_credentials.success_code:
        self.label_status.setText(result)
        self.label_status.setStyleSheet("color: yellow;")
        return
    elif self.combo_box.currentText() == "Yandex.disk":
      pass

    self.isCancelExit = False
    self.close()

  def addCredentialsInput(self, layout: QVBoxLayout) -> None:
    email_input_layout = QFormLayout()
    label_email_explanation = QLabel("Enter email")
    self.line_edit_email_input = QLineEdit()
    self.line_edit_email_input.setValidator(self.regular_expression_no_spaces)
    email_input_layout.addRow(label_email_explanation, self.line_edit_email_input)

    password_input_layout = QFormLayout()
    label_password_explanation = QLabel("Enter password")
    self.line_edit_password_input = QLineEdit()
    self.line_edit_password_input.setEchoMode(QLineEdit.Password)
    password_input_layout.addRow(label_password_explanation, self.line_edit_password_input)

    layout.addLayout(email_input_layout)
    layout.addLayout(password_input_layout)

  def addTokenInput(self, layout: QVBoxLayout) -> None:
    token_input_layout = QFormLayout()
    label_token_explanation = QLabel("Enter token")
    self.line_edit_token_input = QLineEdit()
    token_input_layout.addRow(label_token_explanation, self.line_edit_token_input)
    layout.addLayout(token_input_layout)

  def getCredentialsWidget(self, service_name: str) -> QWidget:
    result_widget = QWidget()
    widget_layout = QVBoxLayout()
    result_widget.setLayout(widget_layout)

    name_of_storage_layout = QFormLayout()
    label_explanation = QLabel("Enter storage name")
    self.line_edit_storage_name = QLineEdit()
    name_of_storage_layout.addRow(label_explanation, self.line_edit_storage_name)
    widget_layout.addLayout(name_of_storage_layout)

    if service_name == "Mega.nz":
      self.addCredentialsInput(widget_layout)
    elif service_name == "Yandex.disk":
      self.addTokenInput(widget_layout)

    return result_widget

  def comboBoxItemChanged(self, index) -> None:
    self.credentials_widget.setParent(None)
    self.credentials_widget.deleteLater()
    self.credentials_widget = self.getCredentialsWidget(self.combo_box.itemText(index))
    self.layout().insertWidget(1, self.credentials_widget)
