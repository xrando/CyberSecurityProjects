import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider
from PyQt5.QtCore import Qt
from resources.QDropFrame import DropFrame

class DecodePage(QFrame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFrameShape(QFrame.StyledPanel)
    self.setStyleSheet("background-color: white;border:none;");

    # Setting column layout
    col_layout = QHBoxLayout(self)
    col_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0

    contentFrame = QFrame(self, styleSheet="")
    contentFrame.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(contentFrame)
    
    sideFrame = QFrame(self, styleSheet="background-color: #826BFF")
    sideFrame.setFrameShape(QFrame.StyledPanel)
    sideFrame.setFixedWidth(400)
    col_layout.addWidget(sideFrame)

    # ContentFrame layout
    #
    #
    # ContentFrame layout end

    # SideFrame layout
    sideFrameLayout = QVBoxLayout(sideFrame)
    sideFrameLayout.setAlignment(Qt.AlignTop)
    sideFrameLayout.setContentsMargins(30,10,30,10)

    sliderLabel = QLabel("SELECT LSB", sideFrame, styleSheet="font-size:20px;font-weight:bold;font-family:Arial,sans-serif;")

    self.slider = QSlider(Qt.Horizontal)
    self.slider.setRange(1, 6)  # Set the range from 0 to 5 (6 options)
    self.slider.setTickInterval(1)  # Set the tick interval to 1
    self.slider.setTickPosition(QSlider.TicksBelow)  # Show ticks below the slider

    label = QLabel("1",styleSheet="font-size:28px;font-weight:bold;font-family:Arial,sans-serif;")

    self.slider.valueChanged.connect(lambda value: label.setText(f"{value}   "))

    slider_layout = QHBoxLayout()
    slider_layout.addWidget(self.slider)
    slider_layout.addWidget(label)

    sideFrameLayout.addWidget(sliderLabel)
    sideFrameLayout.addLayout(slider_layout)
    sideFrameLayout.addSpacing(20)
    # SideFrame layout end


