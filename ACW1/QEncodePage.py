from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from resources.QDropFrame import DropFrame
from resources.QCustomButton import CustomButton
from steganography.image.StegnoImg import imgSteg
from steganography.Utilities import read_file_content
import cv2, time, os, shutil

class EncodePage(QFrame):
  def __init__(self, parent=None):
    super().__init__(parent)
    self.setFrameShape(QFrame.StyledPanel)
    self.setStyleSheet("background-color: white;border:none;");

    # Setting column layout
    col_layout = QHBoxLayout(self)
    col_layout.setContentsMargins(0, 0, 0, 0)  # Set margins to 0

    payloadFrame = QFrame(self)
    payloadFrame.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(payloadFrame)

    coverFrame = QFrame(self)
    coverFrame.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(coverFrame)

    sideFrame = QFrame(self, styleSheet="background-color: #FF7E4B")
    sideFrame.setFrameShape(QFrame.StyledPanel)
    sideFrame.setFixedWidth(400)
    col_layout.addWidget(sideFrame)

    # payloadColFrame layout
    payloadFrameLayout = QVBoxLayout(payloadFrame)
    payloadFrameLayout.setAlignment(Qt.AlignTop)
    payloadDndLabel = QLabel("TEXT DOCUMENT INPUT", payloadFrame, styleSheet="font-size:20px;font-weight:bold;font-family:Arial,sans-serif;")
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

    # coverColFrame layout
    coverFrameLayout = QVBoxLayout(coverFrame)
    coverFrameLayout.setAlignment(Qt.AlignTop)

    coverObjDndLabel = QLabel("COVER OBJECT INPUT", payloadFrame, styleSheet="font-size:20px;font-weight:bold;font-family:Arial,sans-serif;")
    coverFrameLayout.addWidget(coverObjDndLabel, alignment=Qt.AlignTop)

    coverObjFeedbackText = QLabel("", coverFrame)
    coverObjDisplayIcon = QLabel("", coverFrame)

    self.coverObjDraggable = DropFrame(coverFrame, 
      feedbackLabel = coverObjFeedbackText, 
      displayFileIcon = coverObjDisplayIcon,
      allowedExtensions = [".txt", ".csv", ".docx", ".jpg", ".png", ".bmp", ".gif"]
    )
    self.coverObjDraggable.setFixedHeight(250)

    coverFrameLayout.addWidget(self.coverObjDraggable)
    coverFrameLayout.addWidget(coverObjFeedbackText)
    coverFrameLayout.addWidget(coverObjDisplayIcon)
    # coverColFrame layout end

    # SideFrame layout
    sideFrameLayout = QVBoxLayout(sideFrame)
    sideFrameLayout.setAlignment(Qt.AlignTop)
    sideFrameLayout.setContentsMargins(30,10,30,10)

    sliderLabel = QLabel("SELECT LSB", sideFrame, styleSheet="font-size:20px;font-weight:bold;font-family:Arial,sans-serif;")

    self.slider = QSlider(Qt.Horizontal)
    self.slider.setRange(1, 6)  # Set the range from 0 to 5 (6 options)
    self.slider.setTickInterval(1)  # Set the tick interval to 1
    self.slider.setTickPosition(QSlider.TicksBelow)  # Show ticks below the slider

    sliderValue = QLabel("1",styleSheet="font-size:28px;font-weight:bold;font-family:Arial,sans-serif;")

    self.slider.valueChanged.connect(lambda value: sliderValue.setText(f"{value}"))

    slider_layout = QHBoxLayout()
    slider_layout.addWidget(self.slider)
    slider_layout.addWidget(sliderValue)
    
    encodeButton = CustomButton("ENCODE", sideFrame)
    encodeButton.clicked.connect(self.encodeFile)

    self.encodeFeedbackLabel = QLabel("", sideFrame)
    self.encodeFeedbackImage = QLabel("", sideFrame, visible=False)
    # self.encodeFeedbackAudio 

    self.downloadEncodedButton = CustomButton("DOWNLOAD", sideFrame, visible=False)
    self.downloadEncodedButton.clicked.connect(self.downloadEncodedFile)

    sideFrameLayout.addWidget(sliderLabel)
    sideFrameLayout.addLayout(slider_layout)
    sideFrameLayout.addSpacing(20)
    sideFrameLayout.addWidget(encodeButton)
    sideFrameLayout.addSpacing(20)
    sideFrameLayout.addWidget(self.encodeFeedbackLabel)
    sideFrameLayout.addWidget(self.encodeFeedbackImage)
    sideFrameLayout.addSpacing(20)
    sideFrameLayout.addWidget(self.downloadEncodedButton)
    # SideFrame layout end


  def downloadEncodedFile(self):
    # Get the source_file_path 
    source_file_path = f"output/{self.filename}"

    # Get the source file extension
    source_extension = os.path.splitext(source_file_path)[1]

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
      shutil.copy(source_file_path, destination_file_path)

  def encodeFile(self):
    self.resetFeedback()
    payloadPath, payloadType = self.payloadDraggable.value
    coverObjPath, coverObjType = self.coverObjDraggable.value
    print(payloadPath, payloadType, coverObjPath, coverObjType)
    print(self.slider.value())

    if payloadPath is None or payloadType is None:
      self.encodeFeedbackLabel.setText("Invalid input.")
      return
    
    if coverObjType in [".jpg", ".bmp", ".png", ".gif"]:
      # For image type encoding
      imageSteganography = imgSteg()
      encoded_image = imageSteganography.encode(img=coverObjPath, message=read_file_content(payloadPath), bits=self.slider.value())
      self.filename = f"img-{int(time.time())}{coverObjType}"

      self.encodeFeedbackLabel.setText(f"Encoded Object: {self.filename}")
      self.displayFeedbackImage(encoded_image, self.filename)

      self.downloadEncodedButton.setVisible(True)
    elif coverObjType in [".txt", ".xls",".docx"]:
      # For document type encoding
      self.encodeFeedbackLabel.setText(f"Encoded Object: doc-{int(time.time())}{coverObjType}")
      self.downloadEncodedButton.setVisible(True)
      pass
    elif coverObjType in [".mp3", ".mp4", ".wav"]:
      # For audio type encoding
      self.encodeFeedbackLabel.setText(f"Encoded Object: aud-{int(time.time())}{coverObjType}")
      self.downloadEncodedButton.setVisible(True)
      pass
    else:
      self.encodeFeedbackLabel.setText("Invalid input.")
    pass

  def displayFeedbackImage(self, encoded_image, filename):
    # Convert the BGR image to RGB (if necessary)
    image_rgb = cv2.cvtColor(encoded_image, cv2.COLOR_BGR2RGB)
    # Create a QImage from the RGB image data
    height, width, channel = image_rgb.shape
    qimage = QImage(image_rgb.data, width, height, width * channel, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)
  
    # Save the QPixmap object as an image file
    pixmap.save(f"output/{filename}")

    fixed_height = 100  # Specify the desired fixed height

    # Calculate the width based on the aspect ratio
    aspect_ratio = pixmap.width() / pixmap.height()
    fixed_width = int(fixed_height * aspect_ratio)

    pixmap = pixmap.scaled(fixed_width, fixed_height, Qt.AspectRatioMode.KeepAspectRatio)
    self.encodeFeedbackImage.setPixmap(pixmap)
    self.encodeFeedbackImage.setVisible(True)
  
  def resetFeedback(self):    
    self.encodeFeedbackLabel.setText("")
    self.encodeFeedbackImage.clear()
    self.encodeFeedbackImage.setVisible(False)
    self.downloadEncodedButton.setVisible(False)

