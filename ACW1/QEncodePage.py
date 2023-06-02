from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame, QSlider, QFileDialog, QFileIconProvider
from PyQt5.QtCore import Qt, QFileInfo
from PyQt5.QtGui import QPixmap, QImage
from resources.QDropFrame import DropFrame
from resources.QCustomButton import CustomButton
from resources.QAudioPlayer import AudioPlayer
from steganography.Image import imgSteg
from steganography.Utilities import read_file_content
from steganography.Audio import audioSteg
from steganography.wordDoc import fontcolourSteganography
import cv2, time, os, shutil, imageio

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
      allowedExtensions = [".txt", ".xlsx"]
    )
    self.payloadDraggable.setFixedHeight(250)

    payloadFrameLayout.addWidget(self.payloadDraggable)
    payloadFrameLayout.addWidget(payloadFeedbackText)
    payloadFrameLayout.addWidget(payloadDisplayIcon)
    # payloadColFrame layout end

    # coverColFrame layout
    coverFrameLayout = QVBoxLayout(coverFrame)
    coverFrameLayout.setAlignment(Qt.AlignTop)

    coverObjDndLabel = QLabel("COVER OBJECT INPUT", coverFrame, styleSheet="font-size:20px;font-weight:bold;font-family:Arial,sans-serif;")
    coverFrameLayout.addWidget(coverObjDndLabel, alignment=Qt.AlignTop)

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

    self.mediaPlayerFeedback = AudioPlayer(sideFrame)
    # Show the main window
    self.mediaPlayerFeedback.hide()

    sideFrameLayout.addWidget(sliderLabel)
    sideFrameLayout.addLayout(slider_layout)
    sideFrameLayout.addSpacing(20)
    sideFrameLayout.addWidget(encodeButton)
    sideFrameLayout.addSpacing(20)
    sideFrameLayout.addWidget(self.encodeFeedbackLabel)
    sideFrameLayout.addWidget(self.encodeFeedbackImage)
    sideFrameLayout.addWidget(self.mediaPlayerFeedback)
    sideFrameLayout.addSpacing(20)
    sideFrameLayout.addWidget(self.downloadEncodedButton)
    # SideFrame layout end


  def downloadEncodedFile(self):

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

  def encodeFile(self):
    try:
      self.resetFeedback()
      payloadPath, payloadType = self.payloadDraggable.value
      coverObjPath, coverObjType = self.coverObjDraggable.value

      if payloadPath is None or payloadType is None:
        self.encodeFeedbackLabel.setText("Invalid input.")
        return
      
      if coverObjType in [".jpg", ".bmp", ".png", ".gif"]:
        # For image type encoding
        filename = f"img-{int(time.time())}{coverObjType}"
        self.source_file_path = f"output/encoded/{filename}"

        # Initialize the image steganography object
        imgS = imgSteg()

        # Begin encoding the payload with cover object
        encoded_image = imgS.encode(img=coverObjPath, message=read_file_content(payloadPath), bits=self.slider.value())

        # Save the output image (encoded image)
        imageio.mimsave(self.source_file_path, encoded_image,loop = 0)

        self.encodeFeedbackLabel.setText(f"Encoded Object: {filename}")
        self.displayFeedbackImage()

        self.downloadEncodedButton.setVisible(True)

      elif coverObjType in [".txt"]:

        # For document type encoding
        self.encodeFeedbackLabel.setText(f"Encoded Object: doc-{int(time.time())}{coverObjType}")
        self.downloadEncodedButton.setVisible(True)
        pass
      elif coverObjType in [".docx"]:
        # For document type encoding
        filename = f"doc-{int(time.time())}{coverObjType}"
        self.encodeFeedbackLabel.setText(f"Encoded Object: {filename}")
        self.source_file_path = f"output/encoded/{filename}"

        # Initialize the image steganography object
        wordDocS = fontcolourSteganography()

        # Begin encoding the payload with cover object
        encodedDocx = wordDocS.encode(filePath=coverObjPath, payload_file=payloadPath, bit=self.slider.value())
        encodedDocx.save(self.source_file_path)
        self.displayDocFileIcon()
        self.downloadEncodedButton.setVisible(True)


      elif coverObjType in [".mp3", ".mp4", ".wav"]:
        # For audio type encoding
        filename = f"audio-{int(time.time())}{coverObjType}"
        self.source_file_path = f"output/encoded/{filename}"
        audioS = audioSteg()
        audioS.encode(audio_path=coverObjPath,output_path = self.source_file_path, payload_path=payloadPath, num_lsb = self.slider.value())
        self.mediaPlayerFeedback.setAudioPath(self.source_file_path)
        self.mediaPlayerFeedback.show()

        self.encodeFeedbackLabel.setText(f"Encoded Object: {filename}")
        self.downloadEncodedButton.setVisible(True)
        pass
      else:
        self.encodeFeedbackLabel.setText("Invalid input.")

    except Exception as e:
      self.encodeFeedbackLabel.setText(str(e))

  def displayFeedbackImage(self):
    # Load the encoded image using imageio
    encoded_image = imageio.imread(self.source_file_path)
    image_type = self.source_file_path.split(".")[1]

    # Convert the numpy array to a QImage
    height, width, channel = encoded_image.shape
    bytes_per_line = 3 * width
    qimage = QImage(encoded_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)

    fixed_height = 100  # Specify the desired fixed height

    # Calculate the width based on the aspect ratio
    aspect_ratio = pixmap.width() / pixmap.height()
    fixed_width = int(fixed_height * aspect_ratio)

    pixmap = pixmap.scaled(fixed_width, fixed_height, Qt.AspectRatioMode.KeepAspectRatio)
    self.encodeFeedbackImage.setPixmap(pixmap)
    self.encodeFeedbackImage.setVisible(True)
  
  def displayDocFileIcon(self):
    # Use the MIME type to retrieve the appropriate icon
    file_icon_provider = QFileIconProvider()
    icon = file_icon_provider.icon(QFileInfo(self.source_file_path))

    pixmap = icon.pixmap(64, 64)
    pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
    self.encodeFeedbackImage.setPixmap(pixmap)
    self.encodeFeedbackImage.setVisible(True)
  
  def resetFeedback(self):    
    self.encodeFeedbackLabel.setText("")
    self.encodeFeedbackImage.clear()
    self.encodeFeedbackImage.setVisible(False)
    self.downloadEncodedButton.setVisible(False)
    self.mediaPlayerFeedback.stop_audio()
    self.mediaPlayerFeedback.hide()


