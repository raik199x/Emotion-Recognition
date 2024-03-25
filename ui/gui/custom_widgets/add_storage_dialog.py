from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QComboBox, QFormLayout, QLineEdit, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from ui.gui.custom_widgets.dark_style_button import DarkStyleButton
from CloudStorages.cloud_storage_interface import CloudStorageInterface
import config_parser


class AddStorageDialog(QDialog):
  def __init__(self):
    super().__init__()
    # Flags
    self.return_instance = None
    self.return_storage_name = str()

    # Reg exp
    self.regular_expression_no_spaces = QRegularExpressionValidator(QRegularExpression(r"\S+"))
    self.regular_expression_no_spaces_and_dots = QRegularExpressionValidator(QRegularExpression(r"^[^. ]+$"))
    self.regular_expression_no_dots = QRegularExpressionValidator(QRegularExpression(r"^[^.]+$"))

    self.recreateLineEdits()

    # Cloud storage interaction interface
    self.cs_interaction_interface = CloudStorageInterface()

    # Layouts
    self.setWindowTitle("Adding storage")
    main_layout = QVBoxLayout()
    self.setLayout(main_layout)

    storage_provider_layout = QFormLayout()  # start storage_provider_layout

    self.combo_box = QComboBox()
    for item in self.cs_interaction_interface.list_supported_cloud:
      self.combo_box.addItem(item)
    self.combo_box.currentIndexChanged.connect(self.comboBoxItemChanged)

    combo_box_label = QLabel("Choose storage provider: ")
    storage_provider_layout.addRow(combo_box_label, self.combo_box)
    main_layout.addLayout(storage_provider_layout)  # end of storage_provider_layout

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

  def recreateLineEdits(self) -> None:
    # Auth line edits
    self.line_edit_storage_name = QLineEdit()
    self.line_edit_storage_name.setValidator(self.regular_expression_no_dots)

    self.line_edit_email_input = QLineEdit()
    self.line_edit_email_input.setValidator(self.regular_expression_no_spaces)

    self.line_edit_password_input = QLineEdit()
    self.line_edit_token_input = QLineEdit()

  def confirmClicked(self) -> None:
    if len(self.line_edit_storage_name.text()) == 0:
      self.label_status.setText("Storage name is empty!")
      self.label_status.setStyleSheet("color: yellow;")
      return

    cloud_storage = self.cs_interaction_interface.getStorageInstance(self.combo_box.currentText())

    check_auth_result = self.cs_interaction_interface.checkAuthFields(
      cloud_storage,
      self.line_edit_email_input.text(),
      self.line_edit_password_input.text(),
      self.line_edit_token_input.text(),
    )
    if not check_auth_result == self.cs_interaction_interface.success_code:
      self.label_status.setText(check_auth_result)
      self.label_status.setStyleSheet("color: yellow;")
      return

    login_result = self.cs_interaction_interface.tryLogin(
      cloud_storage,
      self.line_edit_email_input.text(),
      self.line_edit_password_input.text(),
      self.line_edit_token_input.text(),
    )
    if not login_result == self.cs_interaction_interface.success_code:
      self.label_status.setText(str(login_result))
      self.label_status.setStyleSheet("color: yellow;")
      return

    credentials_dict = self.cs_interaction_interface.getAuthFields(
      cloud_storage,
      self.line_edit_email_input.text(),
      self.line_edit_password_input.text(),
      self.line_edit_token_input.text(),
    )
    if credentials_dict == self.cs_interaction_interface.fail_code:
      self.label_status.setText("Unexpected error: cloud provider does not support any kind of authentication")
      self.label_status.setStyleSheet("color: yellow;")
      return

    saving_credentials = config_parser.ProjectConfig()
    result = saving_credentials.addStorageEntry(
      self.combo_box.currentText(), self.line_edit_storage_name.text(), credentials_dict
    )
    if not result == saving_credentials.success_code:
      self.label_status.setText(result)
      self.label_status.setStyleSheet("color: yellow")
      return

    # Finalize
    self.return_instance = cloud_storage
    self.return_storage_name = self.line_edit_storage_name.text()
    self.close()

  def addCredentialsInput(self, layout: QVBoxLayout) -> None:
    email_input_layout = QFormLayout()
    label_email_explanation = QLabel("Enter email")
    email_input_layout.addRow(label_email_explanation, self.line_edit_email_input)

    password_input_layout = QFormLayout()
    label_password_explanation = QLabel("Enter password")
    self.line_edit_password_input.setEchoMode(QLineEdit.Password)
    password_input_layout.addRow(label_password_explanation, self.line_edit_password_input)

    layout.addLayout(email_input_layout)
    layout.addLayout(password_input_layout)

  def addTokenInput(self, layout: QVBoxLayout) -> None:
    token_input_layout = QFormLayout()
    label_token_explanation = QLabel("Enter token")
    token_input_layout.addRow(label_token_explanation, self.line_edit_token_input)
    layout.addLayout(token_input_layout)

  def getCredentialsWidget(self, service_name: str) -> QWidget:
    result_widget = QWidget()
    widget_layout = QVBoxLayout()
    result_widget.setLayout(widget_layout)

    name_of_storage_layout = QFormLayout()
    label_explanation = QLabel("Enter storage name")
    name_of_storage_layout.addRow(label_explanation, self.line_edit_storage_name)
    widget_layout.addLayout(name_of_storage_layout)

    cloud_storage = self.cs_interaction_interface.getStorageInstance(service_name)
    if cloud_storage == self.cs_interaction_interface.unknown_code:
      self.label_status.setText("Unknown cloud storage provider")
      self.label_status.setStyleSheet("color: red;")
      return result_widget
    if cloud_storage.isAuthViaCredentials:
      self.addCredentialsInput(widget_layout)
    if cloud_storage.isAuthViaToken:
      self.addTokenInput(widget_layout)

    return result_widget

  def comboBoxItemChanged(self, index) -> None:
    self.label_status.setText("Nothing bad so far")
    self.credentials_widget.setParent(None)
    self.credentials_widget.deleteLater()
    self.recreateLineEdits()
    self.credentials_widget = self.getCredentialsWidget(self.combo_box.itemText(index))
    self.layout().insertWidget(1, self.credentials_widget)
