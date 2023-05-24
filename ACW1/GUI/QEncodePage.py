import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from QDropFrame import DropFrame

class EncodePage(QFrame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFrameShape(QFrame.StyledPanel)
    self.setStyleSheet("background-color: red;")

    col_layout = QHBoxLayout(self)

    colfrm1 = QFrame(self, styleSheet="background-color: grey;")
    colfrm1.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(colfrm1)

    colfrm2 = QFrame(self, styleSheet="background-color: green;")
    colfrm2.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(colfrm2)