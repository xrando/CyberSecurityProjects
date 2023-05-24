import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from QDropFrame import DropFrame

class EncodePage(QFrame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFrameShape(QFrame.StyledPanel)
    self.setStyleSheet("background-color: white;border:none;");

    # Setting column layout
    col_layout = QHBoxLayout(self)
    col_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0

    sideFrame = QFrame(self, styleSheet="background-color: #FF7E4B")
    sideFrame.setFrameShape(QFrame.StyledPanel)
    sideFrame.setFixedWidth(400)
    col_layout.addWidget(sideFrame)

    payloadFrame = QFrame(self, styleSheet="")
    payloadFrame.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(payloadFrame)

    coverFrame = QFrame(self, styleSheet="")
    coverFrame.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(coverFrame)

    # SideFrame layout
    sideFrameLayout = QVBoxLayout(sideFrame)
    encodeLabel = QLabel("Encode", sideFrame, styleSheet="font-size:32px;font-weight:bold;font-family:Arial,sans-serif;color:white;")
  
    sideFrameLayout.addWidget(encodeLabel, alignment=Qt.AlignTop)
    # SideFrame layout end

    # payloadColFrame layout
    payloadFrameLayout = QVBoxLayout(payloadFrame)
    draggable = DropFrame(payloadFrame)
    payloadFrameLayout.addWidget(draggable)
    # payloadColFrame layout end

    # coverColFrame layout
    coverFrameLayout = QVBoxLayout(coverFrame)
    coverFrameLayout.setAlignment(Qt.AlignCenter)
    draggable2 = DropFrame(coverFrame)
    coverFrameLayout.addWidget(draggable2)
    # coverColFrame layout end