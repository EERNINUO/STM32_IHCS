import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (FigureCanvasQTAgg as
            FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from PyQt6.QtWidgets import QSizePolicy

class Paint(FigureCanvas):
    def __init__(self, parent=None) -> None:
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig, self.ax1 = plt.subplots()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Policy.Expanding,
                                   QSizePolicy.Policy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.legend_flag = 0
        plt.xlabel("时间(t)")
        plt.ylabel("温度(℃)")
        plt.xlim(0,60)
        plt.ylim(-10,40)
        self.ax2 = self.ax1.twinx()
        plt.ylabel("湿度(%)")
        plt.ylim(0,100)
        plt.ion()

    def my_draw(self, x, y1, y2):
        self.ax1.plot(x, y1, color= 'r', linestyle= '-', label= '温度')
        plt.grid(color='0.2', linestyle= '--')
        self.ax2.plot(x, y2, color= 'b', linestyle= '--', label= '湿度')
        if self.legend_flag == 0:
            self.ax1.legend(bbox_to_anchor= (1, 1))
            self.ax2.legend(bbox_to_anchor= (1, 0.9))
            self.legend_flag += 1

    def end_draw(self):
        plt.close("all")

