from PyQt5.QtWidgets import QPushButton

class CustomButton(QPushButton):
    def __init__(self, text, parent=None, visible=True):
        super().__init__(text, parent, visible=visible)
        self.setFixedHeight(40)
        self.setObjectName("pushButton")
        self.setStyleSheet( 
            "#pushButton{" +
            "background-color:#CCCCCC;" +
            "border: 2px solid #484848;" + 
            "border-bottom-width: 4px;" +
            "font-size:20px;" +
            "font-weight:bold;" +
            "font-family:Arial,sans-serif;}" +

            "#pushButton:hover {" +
            "background-color: #BBBBBB;" +
            "border-color: #383838;}" +

            "#pushButton:pressed{" +
            "background-color: #AAAAAA;" +
            "border-color: #282828;}"
        )