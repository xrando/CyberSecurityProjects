from PyQt5.QtWidgets import QVBoxLayout, QLabel, QFrame, QFileDialog, QFileIconProvider
from PyQt5.QtCore import Qt, pyqtSignal, QFileInfo
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent, QPixmap
import os

dropFrameStyle = ("#DropFrame{" +
  "background-color: rgba(230,230,230,0.4);" +                  
  "border:10px dashed #DAFF8A;" +
  "border-radius:20px;}" +
  "QLabel { background-color:transparent;}"
)

frameEnterStyle = ("#DropFrame{"+
  "background-color: rgba(218,255,138,0.1);" +
  "border:10px dashed #DAFF8A;" +
  "border-radius:20px;}" +
  "QLabel { background-color:transparent;}"
)

class DropFrame(QFrame):
  # Define a signal
  enableSlider = pyqtSignal(bool)

  def __init__(self, parent=None, feedbackLabel=None, displayFileIcon=None, allowedExtensions=[], noLSB=None):
    super().__init__(parent)

    self.feedbackLabel = feedbackLabel
    self.displayFileIcon = displayFileIcon
    self.allowedExtensions = allowedExtensions
    self.noLSB = noLSB
    self.value = None, None # file_path, file_type

    self.setObjectName("DropFrame")
    self.setStyleSheet(dropFrameStyle)

    # Set this widget to be a drag and drop
    self.setAcceptDrops(True)
    self.setFrameShape(QFrame.StyledPanel)

    # Set this widget to allow cursor changing
    self.setMouseTracking(True)
    self.setCursor(Qt.ArrowCursor)

    layout = QVBoxLayout(self)
    layout.setAlignment(Qt.AlignCenter)

    # Create download icon at the center of the dnd component
    pixmap = QPixmap('./resources/image/download.png')
    pixmap = pixmap.scaled(90, 60, Qt.AspectRatioMode.KeepAspectRatio)
    downloadIcon = QLabel("Drag and Drop Files Here", self)
    downloadIcon.setPixmap(pixmap)
    layout.addWidget(downloadIcon, alignment= Qt.AlignCenter)

    # Create the label below download icon
    label = QLabel("Drag and Drop Files Here", self)
    layout.addWidget(label)

  def dragEnterEvent(self, event: QDragEnterEvent):
    self.setStyleSheet(frameEnterStyle)

    if event.mimeData().hasUrls():
      event.acceptProposedAction()

  def dropEvent(self, event: QDropEvent):
    self.setStyleSheet(dropFrameStyle)
    if not event.mimeData().hasUrls():
      event.ignore()

    file_paths = [url.toLocalFile() for url in event.mimeData().urls()]

    if len(file_paths) > 1:
      self.feedbackLabel.setText("Please drop only one file.")
      event.ignore()

    file_path = file_paths[0]

    if self.processFileInput(file_path):
      event.acceptProposedAction()
    else:
      event.ignore()
      
  def enterEvent(self, event):
    self.setCursor(Qt.PointingHandCursor)
    super().enterEvent(event)
    
  def leaveEvent(self, event):
    self.setCursor(Qt.ArrowCursor)
    super().leaveEvent(event)

  def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
      file_dialog = QFileDialog()
      file_dialog.setFileMode(QFileDialog.AnyFile)
      file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
      if file_dialog.exec_() == QFileDialog.Accepted:
        selected_file = file_dialog.selectedFiles()[0]
        self.processFileInput(selected_file)  
    
    # Call the base class implementation
    super().mousePressEvent(event)

  def dragLeaveEvent(self, event: QDragLeaveEvent):
    self.setStyleSheet(dropFrameStyle)

  def processFileInput(self, file_path):
    self.displayFileIcon.clear()
    file_extension = os.path.splitext(file_path)[1]
    file_name = os.path.basename(file_path)

    # Check if the file extension is in the list of allowed extensions

    if file_extension in self.allowedExtensions:
      self.feedbackLabel.setText(f"Uploaded File: {file_name}\nFile Type: {file_extension}")
      # Use the MIME type to retrieve the appropriate icon
      file_icon_provider = QFileIconProvider()
      icon = file_icon_provider.icon(QFileInfo(file_path))

      pixmap = icon.pixmap(64, 64)
      pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
      self.displayFileIcon.setPixmap(pixmap)
      self.value = file_path, file_extension # file_path, file_type

      self.enableSlider.emit(self.noLSB is None or file_extension not in self.noLSB)
      return True
    else:       
      self.setStyleSheet(dropFrameStyle)
      self.feedbackLabel.setText(f"Please use valid file extension")
      self.value = None, None # file_path, file_type
      return False
