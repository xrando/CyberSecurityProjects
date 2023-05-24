import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from QDropFrame import DropFrame
from QEncodePage import EncodePage
from QDecodePage import DecodePage
import mimetypes

app = QApplication(sys.argv)

global uiWidth, uiHeight, uiPositionX, uiPositionY

uiWidth = 750
uiHeight = 900
uiPositionX = 50
uiPositionY = 100

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("Steg Application")
    self.setGeometry(uiPositionX, uiPositionY, uiWidth, uiHeight)
    self.setFixedSize(uiWidth, uiHeight)

    main_widget = QWidget(self)
    self.setCentralWidget(main_widget)
    main_layout = QVBoxLayout(main_widget)
    
    encodePage = EncodePage(self)
    main_layout.addWidget(encodePage)

    decodePage = DecodePage(self)
    main_layout.addWidget(decodePage)

    self.show()

window = MainWindow()

sys.exit(app.exec_())