import matplotlib.pyplot as plt
import time
from multiprocessing import Process, Event

class Paint():
    def __init__(self) -> None:
        self.fix, self.ax1 = plt.subplots()
        self.legend_flag = 0
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        plt.xlabel("时间(t)")
        plt.ylabel("温度(℃)")
        plt.xlim(0,60)
        plt.ylim(-10,40)
        self.ax2 = self.ax1.twinx()
        plt.ylabel("湿度(%)")
        plt.ylim(0,100)
        plt.ion()
        plt.show()

    def draw(self, x, y1, y2):
        self.ax1.plot(x, y1, color= 'r', linestyle= '-', label= '温度')
        plt.grid(color='0.2', linestyle= '--')
        self.ax2.plot(x, y2, color= 'b', linestyle= '--', label= '湿度')
        if self.legend_flag == 0:
            self.ax1.legend(bbox_to_anchor= (1, 1))
            self.ax2.legend(bbox_to_anchor= (1, 0.9))
            self.legend_flag += 1

    def end_draw(self):
        plt.close("all")
