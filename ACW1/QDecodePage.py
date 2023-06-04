import sys
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider, QFileDialog, QFileIconProvider
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QPixmap, QImage
from resources.QDropFrame import DropFrame
from resources.QCustomButton import CustomButton
from resources.QAudioPlayer import AudioPlayer
from steganography.Image import imgSteg
from steganography.Utilities import read_file_content
from steganography.Audio import audioSteg
import cv2, time, os, shutil, imageio


class DecodePage(QFrame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFrameShape(QFrame.StyledPanel)
    self.setStyleSheet("background-color: white;border:none;");

    # Setting column layout
    col_layout = QHBoxLayout(self)
    col_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0

    contentFrame = QFrame(self)
    contentFrame.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(contentFrame)
    
    sideFrame = QFrame(self, styleSheet="background-color: #826BFF")
    sideFrame.setFrameShape(QFrame.StyledPanel)
    sideFrame.setFixedWidth(400)
    col_layout.addWidget(sideFrame)

    # ContentFrame layout
    contentFrameLayout = QVBoxLayout(contentFrame)
    contentFrameLayout.setAlignment(Qt.AlignTop)

    encodedObjDndLabel = QLabel("ENCODED OBJECT INPUT", contentFrame, styleSheet="font-size:20px;font-weight:bold;font-family:Arial,sans-serif;")
    contentFrameLayout.addWidget(encodedObjDndLabel, alignment=Qt.AlignTop)

    encodedObjFeedbackText = QLabel("", contentFrame)
    encodedObjDisplayIcon = QLabel("", contentFrame)

    self.encodedObjDraggable = DropFrame(contentFrame, 
      feedbackLabel = encodedObjFeedbackText, 
      displayFileIcon = encodedObjDisplayIcon,
      allowedExtensions = [".txt", ".csv", ".docx", ".jpg", ".png", ".bmp", ".gif", ".mp3", ".mp4", ".wav"]
    )
    self.encodedObjDraggable.setFixedHeight(250)

    contentFrameLayout.addWidget(self.encodedObjDraggable)
    contentFrameLayout.addWidget(encodedObjFeedbackText)
    contentFrameLayout.addWidget(encodedObjDisplayIcon)
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

    self.slider.valueChanged.connect(lambda value: label.setText(f"{value}"))

    slider_layout = QHBoxLayout()
    slider_layout.addWidget(self.slider)
    slider_layout.addWidget(label)

    decodeButton = CustomButton("DECODE", sideFrame)
    decodeButton.clicked.connect(self.decodeFile)

    self.decodeFeedbackLabel = QLabel("", sideFrame)
    self.decodeFeedbackImage = QLabel("", sideFrame, visible=False)
    # self.DecodeFeedbackAudio 

    self.downloadDecodedButton = CustomButton("DOWNLOAD", sideFrame, visible=False)
    self.downloadDecodedButton.clicked.connect(self.downloadDecodedFile)

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

  def downloadDecodedFile(self):

    # Get the source file extension
    source_extension = os.path.splitext(self.source_file_path)[1]

    # Create the file type filter based on the source file extension
    file_type_filter = f"{source_extension.upper()} Files (*{source_extension})"

    # Open the file dialog to let the user choose the save location
    save_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", file_type_filter)

    if save_path:
      # Get the destination folder and filename from the save_path
      destination_folder = os.path.dirname(save_path)
      filename = os.path.basename(save_path)

      # Create the destination file path
      destination_file_path = os.path.join(destination_folder, filename)

      # Copy the source file to the destination file path
      shutil.copy(self.source_file_path, destination_file_path)



  def decodeFile(self):
      try:
          self.resetFeedback()
          encodedObjPath, encodedObjType = self.encodedObjDraggable.value

          if encodedObjPath is None or encodedObjType is None:
              self.decodeFeedbackLabel.setText("Invalid input.")
              return

          filename = f"decodedmsg-{int(time.time())}.txt"
          self.source_file_path = f"output/decoded/{filename}"

          if encodedObjType in [".jpg", ".bmp", ".png", ".gif"]:
            # Initialize the image steganography object
            imgS = imgSteg()

            # Begin decoding the object
            decoded_data = imgS.decode(img=encodedObjPath, bits=self.slider.value())

            if decoded_data is not None:
              with open(self.source_file_path, 'w') as file:
                file.write(decoded_data)
              self.decodeFeedbackLabel.setText(f"Decoded Object: {filename}")
              self.displayDocFileIcon()
              self.downloadDecodedButton.setVisible(True)
            else:
              self.decodeFeedbackLabel.setText("No hidden message found.")

          elif encodedObjType in [".txt", ".xls", ".docx"]:
              
              # For document type decoding
              self.decodeFeedbackLabel.setText(f"Decoded Object: {filename}")
              # self.decodeFeedbackLabel.setText("Decoding document type is not supported.")
              self.downloadDecodedButton.setVisible(True)
              pass
                     
          elif encodedObjType in [".mp3", ".mp4", ".wav"]:
              audioS = audioSteg()
              # audioS.encode(audio_path=encodedObjPath,output_path = self.source_file_path, payload_path=payloadPath, num_lsb = self.slider.value())
              audioS.decode(audio_path=encodedObjPath, output_path=self.source_file_path, num_lsb=self.slider.value())

              self.decodeFeedbackLabel.setText(f"Decoded Object: {filename}")
              self.displayDocFileIcon()
              self.downloadDecodedButton.setVisible(True)
          else:
            self.decodeFeedbackLabel.setText("Invalid input.")

          #     audioS = audioSteg()
          #     decoded_message = audioS.decode(audio_path=sourceObjPath)

          #     if decoded_message is not None:
          #         self.decodeFeedbackLabel.setText("Decoded Message:")
          #         self.displayDecodedText(decoded_message)
          #     else:
          #         self.decodeFeedbackLabel.setText("No hidden message found.")

          # else:
          #     self.decodeFeedbackLabel.setText("Invalid input.")

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

  def displayDocFileIcon(self):
    # Use the MIME type to retrieve the appropriate icon
    file_icon_provider = QFileIconProvider()
    icon = file_icon_provider.icon(QFileInfo(self.source_file_path))

    pixmap = icon.pixmap(64, 64)
    pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
    self.decodeFeedbackImage.setPixmap(pixmap)
    self.decodeFeedbackImage.setVisible(True)

  def resetFeedback(self):
    self.decodeFeedbackLabel.setText("")
    self.decodeFeedbackImage.clear()
    self.decodeFeedbackImage.setVisible(False)
    self.downloadDecodedButton.setVisible(False)