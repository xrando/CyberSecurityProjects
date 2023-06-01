import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from resources.QDropFrame import DropFrame
from resources.QCustomButton import CustomButton
from resources.QAudioPlayer import AudioPlayer
from steganography.image.StegnoImg import imgSteg
from steganography.Utilities import read_file_content
from steganography.audio.StegnoAudio import audioSteg
import cv2, time, os, shutil, imageio


class DecodePage(QFrame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFrameShape(QFrame.StyledPanel)
    self.setStyleSheet("background-color: white;border:none;");

    # Setting column layout
    col_layout = QHBoxLayout(self)
    col_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0

    payloadFrame = QFrame(self, styleSheet="")
    payloadFrame.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(payloadFrame)

    coverFrame = QFrame(self)
    coverFrame.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(coverFrame)
    
    sideFrame = QFrame(self, styleSheet="background-color: #826BFF")
    sideFrame.setFrameShape(QFrame.StyledPanel)
    sideFrame.setFixedWidth(400)
    col_layout.addWidget(sideFrame)

    # payloadColFrame layout
    payloadFrameLayout = QVBoxLayout(payloadFrame)
    payloadFrameLayout.setAlignment(Qt.AlignTop)
    payloadDndLabel = QLabel("ENCODED TEXT DOCUMENT INPUT", payloadFrame, styleSheet="font-size:20px;font-weight:bold;font-family:Arial,sans-serif;")
    payloadFrameLayout.addWidget(payloadDndLabel, alignment=Qt.AlignTop)

    payloadFeedbackText = QLabel("", coverFrame)
    payloadDisplayIcon = QLabel("", coverFrame)

    self.payloadDraggable = DropFrame(payloadFrame, 
      feedbackLabel = payloadFeedbackText, 
      displayFileIcon = payloadDisplayIcon,
      allowedExtensions = [".txt"]
    )
    self.payloadDraggable.setFixedHeight(250)

    payloadFrameLayout.addWidget(self.payloadDraggable)
    payloadFrameLayout.addWidget(payloadFeedbackText)
    payloadFrameLayout.addWidget(payloadDisplayIcon)
    # payloadColFrame layout end

    # ContentFrame layout
    coverFrameLayout = QVBoxLayout(coverFrame)
    coverFrameLayout.setAlignment(Qt.AlignTop)

    coverObjFeedbackText = QLabel("", coverFrame)
    coverObjDisplayIcon = QLabel("", coverFrame)

    self.coverObjDraggable = DropFrame(coverFrame, 
      feedbackLabel = coverObjFeedbackText, 
      displayFileIcon = coverObjDisplayIcon,
      allowedExtensions = [".txt", ".csv", ".docx", ".jpg", ".png", ".bmp", ".gif", ".mp3", ".mp4", ".wav"]
    )
    self.coverObjDraggable.setFixedHeight(250)

    coverFrameLayout.addWidget(self.coverObjDraggable)
    coverFrameLayout.addWidget(coverObjFeedbackText)
    coverFrameLayout.addWidget(coverObjDisplayIcon)
    
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

    decodeButton = CustomButton("DECODE", sideFrame)
    decodeButton.clicked.connect(self.decodeFile)

    self.decodeFeedbackLabel = QLabel("", sideFrame)
    self.decodeFeedbackImage = QLabel("", sideFrame, visible=False)
    # self.encodeFeedbackAudio 

    self.downloadDecodedButton = CustomButton("DOWNLOAD", sideFrame, visible=False)
    #self.downloadDecodedButton.clicked.connect(self.downloadDecodedFile)

    self.mediaPlayerFeedback = AudioPlayer(sideFrame)
    # Show the main window
    self.mediaPlayerFeedback.hide()


    sideFrameLayout.addWidget(sliderLabel)
    sideFrameLayout.addLayout(slider_layout)
    sideFrameLayout.addSpacing(20)
    sideFrameLayout.addWidget(decodeButton)
    sideFrameLayout.addSpacing(20)
    sideFrameLayout.addWidget(self.decodeFeedbackLabel)
    sideFrameLayout.addWidget(self.decodeFeedbackImage)
    sideFrameLayout.addWidget(self.mediaPlayerFeedback)
    sideFrameLayout.addSpacing(20)
    sideFrameLayout.addWidget(self.downloadDecodedButton)
    # SideFrame layout end


  def decodeFile(self):
      try:
          self.resetFeedback()
          sourceObjPath, sourceObjType = self.sourceObjDraggable.value

          if sourceObjPath is None or sourceObjType is None:
              self.decodeFeedbackLabel.setText("Invalid input.")
              return

          if sourceObjType in [".jpg", ".bmp", ".png", ".gif"]:
              # For image type decoding
              imgS = imgSteg()
              decoded_message = imgS.decode(img=sourceObjPath)

              if decoded_message is not None:
                  self.decodeFeedbackLabel.setText("Decoded Message:")
                  self.displayDecodedText(decoded_message)
              else:
                  self.decodeFeedbackLabel.setText("No hidden message found.")

          elif sourceObjType in [".txt", ".xls", ".docx"]:
              # For document type decoding
              self.decodeFeedbackLabel.setText("Decoding document type is not supported.")

          elif sourceObjType in [".mp3", ".mp4", ".wav"]:
              # For audio type decoding
              audioS = audioSteg()
              decoded_message = audioS.decode(audio_path=sourceObjPath)

              if decoded_message is not None:
                  self.decodeFeedbackLabel.setText("Decoded Message:")
                  self.displayDecodedText(decoded_message)
              else:
                  self.decodeFeedbackLabel.setText("No hidden message found.")

          else:
              self.decodeFeedbackLabel.setText("Invalid input.")

      except Exception as e:
          self.decodeFeedbackLabel.setText(str(e))

  def displayFeedbackImage(self):
    # Load the decoded image using imageio
    decoded_image = imageio.imread(self.source_file_path)
    # Convert the numpy array to a QImage
    height, width, channel = decoded_image.shape
    bytes_per_line = 3 * width
    qimage = QImage(decoded_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)

    fixed_height = 100  # Specify the desired fixed height

    # Calculate the width based on the aspect ratio
    aspect_ratio = pixmap.width() / pixmap.height()
    fixed_width = int(fixed_height * aspect_ratio)

    pixmap = pixmap.scaled(fixed_width, fixed_height, Qt.AspectRatioMode.KeepAspectRatio)
    self.decodeFeedbackImage.setPixmap(pixmap)
    self.decodeFeedbackImage.setVisible(True)

  def resetFeedback(self):
    self.decodeFeedbackLabel.setText("")
    self.decodeFeedbackImage.clear()
    self.decodeFeedbackImage.setVisible(False)
    self.downloadDecodedButton.setVisible(False)


