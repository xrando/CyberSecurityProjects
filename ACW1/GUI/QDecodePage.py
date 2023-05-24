import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from QDropFrame import DropFrame

class DecodePage(QFrame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFrameShape(QFrame.StyledPanel)
    self.setStyleSheet("background-color: white;border:none;");

    # Setting column layout
    col_layout = QHBoxLayout(self)
    col_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0

    sideFrame = QFrame(self, styleSheet="background-color: #826BFF")
    sideFrame.setFrameShape(QFrame.StyledPanel)
    sideFrame.setFixedWidth(400)
    col_layout.addWidget(sideFrame)

    contentFrame = QFrame(self, styleSheet="")
    contentFrame.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(contentFrame)

    # SideFrame layout
    sideFrameLayout = QVBoxLayout(sideFrame)
    encodeLabel = QLabel("Decode", sideFrame, styleSheet="font-size:32px;font-weight:bold;font-family:Arial,sans-serif;color:white;")
  
    sideFrameLayout.addWidget(encodeLabel, alignment=Qt.AlignTop)

    # SideFrame layout end

    # ContentFrame layout
    #
    #
    # ContentFrame layout end


