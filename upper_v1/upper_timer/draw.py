import matplotlib.pyplot as plt
from PyQt6.QtCore import QTimer

class Timer():
    def __init__(self) -> None:
        pass

class Paint():
    def __init__(self) -> None:
        self.timer = QTimer()
        self.fix, self.ax1 = plt.subplots()
        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False
        plt.xlabel("时间(t)")
        plt.ylabel("温度(℃)")
        plt.xlim(0,60)
        plt.ylim(-10,40)
        self.ax2 = self.ax1.twinx()
        plt.ylabel("湿度(%)")
        plt.ylim(0,100)
        plt.legend()
        plt.ion()
        plt.show()

    def draw(self, x, y1, y2):
        plt.clf()
        self.ax1.plot(x, y1, 'r')
        self.ax1.grid(color='0.2', linestyle= '--')
        self.ax2.plot(x, y2, 'b')
        self.ax1.legend(bbox_to_anchor= (1, 1))
        self.ax2.legend(bbox_to_anchor= (1, 0.9))

    def end_draw():
            plt.close("all")

    def draw_begin(self):
        self.timer.start(100)

    def draw_rebegin(self):
        self.timer.start(100)

    def draw_stop(self):
        self.timer.stop()
