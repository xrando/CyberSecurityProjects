from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QDragLeaveEvent, QIcon

class DropFrame(QWidget):
  def __init__(self, parent=None):
    super().__init__(parent)

    # Set this widget to be a drag and drop
    self.setAcceptDrops(True)

    frame = QFrame(self)
    frame.setFrameShape(QFrame.StyledPanel)
    frame.setStyleSheet("border: 3px solid black;")

    layout = QVBoxLayout(frame)
    layout.setAlignment(Qt.AlignCenter)
    label = QLabel("Drag and Drop Files Here", frame)
    label.setStyleSheet("border: 3px solid black;")

    layout.addWidget(label)

  def dragEnterEvent(self, event: QDragEnterEvent):
    if event.mimeData().hasUrls():
      event.acceptProposedAction()

  def dropEvent(self, event: QDropEvent):
    if event.mimeData().hasUrls():
      file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
      self.processDroppedFiles(file_paths)
      event.acceptProposedAction()

  def dragLeaveEvent(self, event: QDragLeaveEvent):
    pass

  def processDroppedFiles(self, file_paths):
    # Implement your logic to process the dropped files here
    for file_path in file_paths:
      print("Dropped file:", file_path)
  def getFileIcon(self, file_path):
    mimetype, _ = mimetypes.guess_type(file_path)
    icon = QIcon.fromTheme(mimetype)
    if icon.isNull():
      icon = QIcon.fromTheme("text-x-generic")  # Fallback icon if no specific icon is found
    return icon

  def displayFileIcon(self, icon):
    pixmap = icon.pixmap(64, 64)
    self.label.setPixmap(pixmap)
    self.label.setScaledContents(True)