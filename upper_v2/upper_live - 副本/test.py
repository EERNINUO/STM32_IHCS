import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from Ui_UI_v2 import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox

class Paint():
    def __init__(self) -> None:
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        self.fix, self.ax1 = plt.subplots()
        self.draw = FigureCanvas(self.fix)


if __name__ == "__main__":
    ui = Ui_MainWindow()
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec())
