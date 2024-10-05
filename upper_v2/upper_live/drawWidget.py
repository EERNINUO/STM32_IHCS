from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget
from draw import Paint

class DrawWidget(QWidget):
    def __init__(self, parent= None) -> None:
        super(DrawWidget, self).__init__(parent)
        self.paint = Paint(parent)
        self.layout.addWidget(self.paint)
    