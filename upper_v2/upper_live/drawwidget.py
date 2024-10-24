from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from draw import Paint

class DrawWidget(QWidget):
    def __init__(self, parent= None) -> None:
        super(DrawWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.paint = Paint(parent)
        self.paint_ntb = NavigationToolbar(self.paint, self)

        self.layout.addWidget(self.paint)
        self.layout.addWidget(self.paint_ntb)
