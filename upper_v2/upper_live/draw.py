import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import (FigureCanvasQTAgg as
            FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtCore import QTimer
from Ui_UI_v2 import Ui_MainWindow
from data import Data
from file import File

class Paint(FigureCanvas):
    def __init__(self, parent=None) -> None:
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = plt.figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.legend_flag = 0
                
        plt.ion()

    def start_my_draw(self, Ui:Ui_MainWindow, Dat_class: Data):
        # try :
            self.dat_class = Dat_class
            plt.clf()
            self.draw_paint()
            self.timer = QTimer(self)
            self.timer.start(1000 // int(Ui.FPSLine.text()))
            self.timer.timeout.connect(self.my_draw)
        # except TypeError:
        #     pass

    def my_draw(self):
        time = self.dat_class.int_time
        if self.dat_class.tem_channel == True :
            y_tem = self.dat_class.tem
            self.tem_ax.plot(time, y_tem, color= 'r', label= '温度')
        if self.dat_class.wet_channel == True :
            y_wet = self.dat_class.wet
            self.wet_ax.plot(time, y_wet, color= 'g', label= '湿度')
        if self.dat_class.channel1_flag == True :
            y_channal1 = self.dat_class.channel1
            self.main_ax.plot(time, y_channal1, color= 'b', label= '通道1')
        if self.dat_class.channel2_flag == True :
            y_channal2 = self.dat_class.channel2
            self.main_ax.plot(time, y_channal2, color= 'b', label= '通道2')
        if self.dat_class.channel3_flag == True :
            y_channal3 = self.dat_class.channel3
            self.main_ax.plot(time, y_channal3, color= 'b', label= '通道3')

        if len(time) > 450 :
            plt.xlim(len(time)*0.1 - 45, len(time)*0.1 + 15)

        if self.legend_flag == 0:
            self.draw_legend()

    def draw_open_file(self, file:File):
        legend_loc = (1, 0.95, 0.9)
        legend_index = 0

        self.main_ax = self.fig.add_subplot()
        plt.ylabel("电压(V)")
        plt.xlabel("时间(s)")
        plt.ylim(0, 3.5)
        plt.xlim(0,60)

        time = list(file.file_dict['time'].values())
        if file.open_file_channel['tem_channel'] == True :
            self.tem_ax = self.main_ax.twinx()
            plt.ylabel("温度(℃)")
            plt.ylim(-10,40)

            y_tem = list(file.file_dict['tem_channel'].values())
            self.tem_ax.plot(time, y_tem, color= 'r', label= '温度')
            self.tem_ax.legend(bbox_to_anchor=(1, legend_loc[legend_index]))
            legend_index += 1
        if file.open_file_channel['wet_channel'] == True :
            self.wet_ax = self.main_ax.twinx()
            plt.ylabel("湿度(%)")
            plt.ylim(0,100)

            y_wet = list(file.file_dict['wet_channel'].values())
            self.wet_ax.plot(time, y_wet, color= 'g', label= '湿度')
            self.wet_ax.legend(bbox_to_anchor=(1, legend_loc[legend_index]))
            legend_index += 1
        if file.open_file_channel['channel1'] == True :
            y_channal1 = list(file.file_dict['channel1'].values())
            self.main_ax.plot(time, y_channal1, color= 'b', label= '通道1')
        if file.open_file_channel['channel2'] == True :
            y_channal2 = list(file.file_dict['channel2'].values())
            self.main_ax.plot(time, y_channal2, color= 'b', label= '通道2')
        if file.open_file_channel['channel3'] == True :
            y_channal3 = list(file.file_dict['channel3'].values())
            self.main_ax.plot(time, y_channal3, color= 'b', label= '通道3')
        self.main_ax.legend(bbox_to_anchor=(1, legend_loc[legend_index]))

        
    def end_draw(self):
        self.timer.stop()
        plt.clf()
        self.legend_flag = 0

    def draw_paint(self):
        self.main_ax = self.fig.add_subplot()
        plt.ylabel("电压(V)")
        plt.xlabel("时间(s)")
        plt.ylim(0, 3.5)
        plt.xlim(0,60)

        if self.dat_class.tem_channel == True:
            self.tem_ax = self.main_ax.twinx()
            plt.ylabel("温度(℃)")
            plt.ylim(-10,40)

        if self.dat_class.wet_channel == True:
            self.wet_ax = self.main_ax.twinx()
            plt.ylabel("湿度(%)")
            plt.ylim(0,100)
        plt.grid(color='0.2', linestyle= '--')

    def draw_legend(self):
        legend_loc = (1, 0.95, 0.9)
        legend_index = 0
        if self.dat_class.tem_channel == True:
            self.wet_ax.legend(bbox_to_anchor=(1, legend_loc[legend_index]))
            legend_index += 1
        if self.dat_class.wet_channel == True:
            self.tem_ax.legend(bbox_to_anchor=(1, legend_loc[legend_index]))
            legend_index += 1
        if (self.dat_class.channel1_flag or 
            self.dat_class.channel2_flag or 
            self.dat_class.channel3_flag) == True:
            self.main_ax.legend(bbox_to_anchor=(1, legend_loc[legend_index]))
            legend_index += 1
        self.legend_flag = 1