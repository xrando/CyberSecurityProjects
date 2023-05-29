import sys
from PyQt5.QtCore import QUrl, Qt, QFileInfo
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QFileIconProvider
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from resources.QCustomButton import CustomButton
from PyQt5.QtGui import QIcon

class AudioPlayer(QWidget):
  def __init__(self, parent=None):
    super(AudioPlayer, self).__init__(parent)
    self.setWindowTitle("Audio Player")

    # Create a layout for the player
    layout = QHBoxLayout(self)
    layout.setContentsMargins(0,0,0,0)

    # Create a QMediaPlayer object
    self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

    # Create a QVideoWidget object to display the audio file
    self.videoWidget = QVideoWidget(self)

    # Set the QVideoWidget as the output for the QMediaPlayer
    self.mediaPlayer.setVideoOutput(self.videoWidget)

    # Create a QLabel for the audio icon
    self.audioIconLabel = QLabel(self)

    # Create a QPushButton for the play button
    self.playButton = CustomButton("Play", self)
    self.playButton.clicked.connect(self.play_audio)

    # Add the video widget, audio icon label, and play button to the layout
    layout.addWidget(self.audioIconLabel)
    layout.addWidget(self.videoWidget)
    layout.addWidget(self.playButton)

  def play_audio(self):
    # Specify the audio file path
    # audio_file = '/path/to/your/audio/file.mp3'

    # Load the audio file into the QMediaPlayer
    if hasattr(self, "audioPath") and self.audioPath is not None:
      audio_path = QUrl.fromLocalFile(self.audioPath)
      self.mediaPlayer.setMedia(QMediaContent(audio_path))

    # Play the audio
    self.mediaPlayer.play()
  
  def setAudioPath(self, audioPath):
    self.audioPath = audioPath

    # Use the MIME type to retrieve the appropriate icon
    file_icon_provider = QFileIconProvider()
    icon = file_icon_provider.icon(QFileInfo(audioPath))

    pixmap = icon.pixmap(64, 64)
    pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio)
    self.audioIconLabel.setPixmap(pixmap)