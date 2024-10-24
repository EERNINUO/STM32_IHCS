import time
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from Ui_UI_v2 import Ui_MainWindow
import stm32

class Data(QThread):    # 用于接受数据的新线程
    warning = pyqtSignal()      # 接受警告信号，发送给警告处理函数
    paint_draw = pyqtSignal()
    def __init__(self, com, Ui:Ui_MainWindow):
        super().__init__()
        self.com = com      # 接受打开的COM口
        self.ui = Ui        # 接受UI
        self.open_flag = True   # 串口打开标志位
        self.time = []
        self.tem = []
        self.wet = []

    def run(self):      # 线程主体
        st_time = time.time()
        while self.open_flag:
            try:
                tem, wet = stm32.trans_data(self.com)   
                if type(tem) == str:        # 判断非正常数据
                    if tem == 'NULL':
                        continue
                    elif tem == 'warning':
                        self.ui.GasLine.setText("含量超标")
                        self.warning.emit()     # 信号广播
                    elif tem == 'end_warning':
                        self.ui.GasLine.setText("正常")
                else:       # 存储正常数据
                    self.tem.append(tem)
                    self.wet.append(wet)
                    self.time.append(time.time() - st_time)
            except TypeError:
                break
