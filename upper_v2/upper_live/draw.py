import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class Paint(FigureCanvas):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.fix, self.ax1 = plt.subplots()
        self.legend_flag = 0
        self.setparent(parent)
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

    def draw(self, x, y1, y2):
        self.ax1.plot(x, y1, color= 'r', linestyle= '-', label= '温度')
        plt.grid(color='0.2', linestyle= '--')
        self.ax2.plot(x, y2, color= 'b', linestyle= '--', label= '湿度')
        if self.legend_flag == 0:
            self.ax1.legend(bbox_to_anchor= (1, 1))
            self.ax2.legend(bbox_to_anchor= (1, 0.9))
            self.legend_flag += 1
        plt.show()

    def end_draw(self):
        plt.close("all")

