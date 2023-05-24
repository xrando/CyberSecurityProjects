import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from QDropFrame import DropFrame
import mimetypes

app = QApplication(sys.argv)

uiWidth = 750
uiHeight = 900
uiPositionX = 50
uiPositionY = 100

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("PyQt5 App")
    self.setGeometry(uiPositionX, uiPositionY, uiWidth, uiHeight)
    self.setFixedSize(uiWidth, uiHeight)

    main_widget = QWidget(self)
    self.setCentralWidget(main_widget)
    main_layout = QVBoxLayout(main_widget)

    frm = QFrame(self, styleSheet="background-color: red;")
    frm.setFrameShape(QFrame.StyledPanel)
    main_layout.addWidget(frm)

    col_layout = QHBoxLayout(frm)

    colfrm1 = QFrame(frm, styleSheet="background-color: grey;")
    colfrm1.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(colfrm1)

    colfrm2 = QFrame(frm, styleSheet="background-color: green;")
    colfrm2.setFrameShape(QFrame.StyledPanel)
    col_layout.addWidget(colfrm2)

    draggable2 = DropFrame(frm)
    main_layout.addWidget(draggable2)

    frm2 = QFrame(self, styleSheet="background-color: blue;")
    frm2.setFrameShape(QFrame.StyledPanel)
    main_layout.addWidget(frm2)

    self.show()

window = MainWindow()

sys.exit(app.exec_())