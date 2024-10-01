# GNU GENERAL PUBLIC LICENSE (GPL) v3.0
# 
# Copyright (c) EERNIINUO
# which is available at https://github.com/EERNINUO/STM32_IHCS
# 
# All rights reserved.

import sys
import serial
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6.QtCore import pyqtSignal
from Ui_UI_v1 import Ui_Form
import data
import draw

open_Serial:serial.Serial
data_thread:data.Data
paint:draw.Paint

def get_serial():
    ports_list = list(serial.tools.list_ports.comports())
    for port in ports_list:
        ui.ComList.addItem(port[1][-5:-1])

def ComCtrl_clicked(): # 打开串口按钮
    if(ui.ComCtrl.text() == "打开串口"):
        global open_Serial # 被打开的串口
        global data_thread #新的线程
        global paint
        try:
            # 打开一个串口
            open_Serial = serial.Serial(ui.ComList.currentText(), 
                    int(ui.BaudRate.currentText()), timeout=0.2)    
            ui.ComCtrl.setText("关闭串口")
            data_thread = data.Data(open_Serial, ui)    # 创建读取数据的线程
            data_thread.start()     # 启动线程
            data_thread.warning.connect(create_QMessageBox)
        
        #检测错误输入
        except serial.serialutil.SerialException:
            QMessageBox.information(None, '', '请选择一个串口',
                                QMessageBox.StandardButton.Ok)
        except ValueError:
            QMessageBox.information(None, '', '请选择一个有效的波特率',
                                QMessageBox.StandardButton.Ok)

    else:
        ui.ComCtrl.setText("打开串口")
        data_thread.open_flag = False
        data_thread.exit()   # 退出线程
        open_Serial.close()  # 关闭串口

def drawing():
    paint.draw(data_thread.time, data_thread.tem, data_thread.wet)

def TemOpen_clicked(): # 温度波形显示按钮
    global paint
    global data_thread
    if(ui.TemOpen.text() == "打开波形显示"):
        ui.TemOpen.setText("关闭波形显示")
        paint = draw.Paint()
        data_thread.paint_draw.connect(drawing)
        data_thread.draw_flag = True
    else: 
        ui.TemOpen.setText("打开波形显示")
        data_thread.draw_flag = False
        paint.end_draw()

def TemCtrl_clicked():      # 
    if(ui.TemCtrl.text() == "暂停波形显示"):
        ui.TemCtrl.setText("继续波形显示")
        data_thread.draw_flag = False
    else:
        ui.TemCtrl.setText("暂停波形显示")
        data_thread.draw_flag = True

def QtEvent():
    ui.ComCtrl.clicked.connect(ComCtrl_clicked) # type: ignore
    ui.TemCtrl.clicked.connect(TemCtrl_clicked) # type: ignore
    ui.TemOpen.clicked.connect(TemOpen_clicked)

def create_QMessageBox():
    QMessageBox.warning(None, '警告', '可燃气体含量超标',
                    QMessageBox.StandardButton.Ok)

if __name__ == "__main__":
    ui = Ui_Form()
    app = QApplication(sys.argv)
    window = QWidget()
    ui.setupUi(window)

    get_serial()
    QtEvent()
    window.show()
    sys.exit(app.exec())