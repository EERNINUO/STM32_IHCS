import time
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import matplotlib.pyplot as plt
from Ui_UI_v1 import Ui_Form
import stm32

class Data(QThread):
    warning = pyqtSignal()
    def __init__(self, com, Ui:Ui_Form):
        super().__init__()
        self.com = com
        self.ui = Ui
        self.open_flag = True
        self.draw_ctrl = False
        self.time = []
        self.tem = []
        self.wet = []

    def run(self):
        begin_time = time.time()
        while self.open_flag:
            try:
                tem, wet = stm32.trans_data(self.com)
                if type(tem) == str:
                    if tem == 'NULL':
                        continue
                    elif tem == 'warning':
                        self.ui.GasLine.setText("含量超标")
                        self.warning.emit()
                    elif tem == 'end_warning':
                        self.ui.GasLine.setText("正常")
                else:
                    self.tem.append(tem)
                    self.wet.append(wet)
                    self.time.append(time.time() - begin_time)
                    self.ui.TemLine.setText(str(tem))
                    self.ui.WetLine.setText(str(wet))
            except TypeError:
                del self.paint
                break

    def draw(self):
        self.paint = Paint()
        self.paint.draw(self.time, self.tem, self.wet)
        plt.show()

class Paint():
    def __init__(self) -> None:
        self.fix, self.ax1 = plt.subplots()
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.xlabel("时间(t)")
        plt.ylabel("温度(℃)")
        plt.xlim(0,60)
        plt.ylim(0,40)
        self.ax2 = self.ax1.twinx()
        plt.ylabel("湿度(%)")
        plt.ylim(0,100)
        plt.ion()

    def draw(self, x, y1, y2):
        self.ax1.plot(x, y1, 'r')
        self.ax2.plot(x, y2, 'b')

def end_draw():
        plt.close("all")
