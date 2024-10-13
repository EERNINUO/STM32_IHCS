import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (FigureCanvasQTAgg as
            FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import QTimer
from data import Data

class Paint(FigureCanvas):
    def __init__(self, parent=None) -> None:
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = plt.figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.legend_flag = 0

        self.ax1 = self.fig.add_subplot()
        plt.xlabel("时间(t)")
        plt.ylabel("温度(℃)")
        plt.xlim(0,60)
        plt.ylim(-10,40)
        self.ax2 = self.ax1.twinx()
        plt.ylabel("湿度(%)")
        plt.ylim(0,100)
        plt.grid(color='0.2', linestyle= '--')
        plt.ion()

    def start_my_draw(self, FPS:int, Dat_class: Data):
        # try :
            self.dat_class = Dat_class
            self.timer = QTimer(self)
            self.timer.start(1000 // FPS)
            self.timer.timeout.connect(self.my_draw)
        # except TypeError:
        #     pass

    def my_draw(self):
        x = self.dat_class.int_time
        y1 = self.dat_class.tem
        y2 = self.dat_class.wet
        self.ax1.plot(x, y1, color= 'r', linestyle= '-', label= '温度')
        self.ax2.plot(x, y2, color= 'b', linestyle= '--', label= '湿度')
        if len(x) > 450 :
            plt.xlim(len(x)*0.1 - 45, len(x)*0.1 + 15)
        if self.legend_flag == 0:
            self.ax1.legend(bbox_to_anchor= (1, 1))
            self.ax2.legend(bbox_to_anchor= (1, 0.9))
            self.legend_flag += 1

    def end_draw(self):
        self.timer.stop()
        plt.clf()
        self.legend_flag = 0

        self.ax1 = self.fig.add_subplot()
        plt.xlabel("时间(t)")
        plt.ylabel("温度(℃)")
        plt.xlabel("时间(t)")
        plt.ylabel("温度(℃)")
        plt.xlim(0,60)
        plt.ylim(-10,40)

        self.ax2 = self.ax1.twinx()
        plt.ylabel("湿度(%)")
        plt.ylim(0,100)
        plt.grid(color='0.2', linestyle= '--')



