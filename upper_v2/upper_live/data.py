import time
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from Ui_UI_v1 import Ui_Form
import draw
import stm32

class Data(QThread):    # 用于接受数据的新线程
    warning = pyqtSignal()      # 接受警告信号，发送给警告处理函数
    paint_draw = pyqtSignal()
    def __init__(self, com, Ui:Ui_Form):
        super().__init__()
        self.com = com      # 接受打开的COM口
        self.ui = Ui        # 接受UI
        self.open_flag = True
        self.draw_flag = False
        self.time = []
        self.tem = []
        self.wet = []

    def run(self):      # 线程主体
        st_time = time.time()
        while self.open_flag:
            try:
                tem, wet = stm32.trans_data(self.com)   
                if type(tem) == str:
                    if tem == 'NULL':
                        continue
                    elif tem == 'warning':
                        self.ui.GasLine.setText("含量超标")
                        self.warning.emit()     # 信号广播
                    elif tem == 'end_warning':
                        self.ui.GasLine.setText("正常")
                else:
                    self.tem.append(tem)
                    self.wet.append(wet)
                    self.time.append(time.time() - st_time)
                    self.ui.TemLine.setText(str(tem))
                    self.ui.WetLine.setText(str(wet))
                    if self.draw_flag :
                        self.paint_draw.emit()
            except TypeError:
                break
