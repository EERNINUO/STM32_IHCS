import time
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from Ui_UI_v2 import Ui_MainWindow
import stm32

class Data(QThread):    # 用于接受数据的新线程
    warning = pyqtSignal()      # 接受警告信号，发送给警告处理函数
    paint_draw = pyqtSignal()
    def __init__(self, com:stm32.STM32, Ui:Ui_MainWindow):
        super().__init__()
        self.com = com      # 接受打开的COM口
        self.ui = Ui        # 接受UI
        self.open_flag = True   # 串口打开标志位
        self.collet_interval = int(self.ui.intervalLine.text())     # 采集间隔
        self.int_time = []
        self.time = []
        self.tem = []
        self.wet = []
        self.channel1 = []
        self.channel2 = []
        self.channel3 = []

    def run(self):      # 线程主体
        st_time = time.time()
        self.channel1_flag = self.ui.channel1.isChecked()
        self.channel2_flag = self.ui.channel2.isChecked()
        self.channel3_flag = self.ui.channel3.isChecked()
        self.tem_channel = self.ui.tem_channel.isChecked()
        self.wet_channel = self.ui.wet_channel.isChecked()
        while self.open_flag:
            try:
                tem, wet, channel1, channel2, channel3= self.com.trans_data(self.com)   
                if type(tem) == str:        # 判断非正常数据
                    if tem == 'NULL':
                        continue
                    elif tem == 'warning':
                        # self.ui.GasLine.setText("含量超标")
                        self.warning.emit()     # 信号广播
                    # elif tem == 'end_warning':
                    #     self.ui.GasLine.setText("正常")
                else:       # 存储正常数据
                    self.int_time.append(time.time() - st_time)
                    self.time.append(f'{self.int_time[-1]:.3f}')
                    self.ui.sampling_time.setText(self.time[-1])
                    if self.tem_channel == True:
                        self.tem.append(tem)
                    if self.wet_channel == True:
                        self.wet.append(wet)
                    if self.channel1_flag == True:
                        self.channel1.append(channel1)
                    if self.channel2_flag == True:
                        self.channel1.append(channel2)
                    if self.channel3_flag == True:
                        self.channel1.append(channel3)
            except TypeError:
                break
