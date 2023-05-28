import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from QEncodePage import EncodePage
from QDecodePage import DecodePage
# from StegnoImg import imgSteg

app = QApplication(sys.argv)

global uiWidth, uiHeight, uiPositionX, uiPositionY

uiWidth = 1200
uiHeight = 950
uiPositionX = 50
uiPositionY = 50

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("Steg Application")
    self.setGeometry(uiPositionX, uiPositionY, uiWidth, uiHeight)
    self.setFixedSize(uiWidth, uiHeight)
    self.setStyleSheet("background-color: #383838;");

    main_widget = QWidget(self)
    self.setCentralWidget(main_widget)
    main_layout = QVBoxLayout(main_widget)
    main_layout.setContentsMargins(0,10,0,0)
    
    encodeTitle = QLabel("Encode", self, styleSheet="font-size:32px;font-weight:bold;font-family:Arial,sans-serif;color:white;")
    encodeTitle.setFixedHeight(40)
    encodeTitle.setContentsMargins(0,10,0,0)
    encodePage = EncodePage(self)

    main_layout.addWidget(encodeTitle)
    main_layout.addWidget(encodePage)

    decodeTitle = QLabel("Decode", self, styleSheet="font-size:32px;font-weight:bold;font-family:Arial,sans-serif;color:white;")
    decodeTitle.setFixedHeight(40)
    decodeTitle.setContentsMargins(0,10,0,0)
    decodePage = DecodePage(self)

    main_layout.addWidget(decodeTitle)
    main_layout.addWidget(decodePage)

    self.show()

window = MainWindow()

sys.exit(app.exec_())