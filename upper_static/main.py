import sys
import serial
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt6 import QtCore
from Ui_UI_v1 import Ui_Form
import data

open_Serial:serial.Serial
data_thread:data.Data

def creat_qmess():
    QMessageBox.warning(None, '警告', '可燃气体含量超标',
                        QMessageBox.StandardButton.Ok)

def get_serial():
    ports_list = list(serial.tools.list_ports.comports())
    for port in ports_list:
        ui.ComList.addItem(port[1][-5:-1])

def ComCtrl_clicked(): # 打开串口按钮
    if(ui.ComCtrl.text() == "打开串口"):
        global open_Serial # 被打开的串口
        global data_thread #新的线程

        try:
            open_Serial = serial.Serial(ui.ComList.currentText(), 
                                int(ui.BaudRate.currentText()), timeout=0.2)
            ui.ComCtrl.setText("关闭串口")
            data_thread = data.Data(open_Serial, ui)
            data_thread.start()
            data_thread.warning.connect(creat_qmess)

        except serial.serialutil.SerialException:
            QMessageBox.information(None, '', '请选择一个串口',
                                QMessageBox.StandardButton.Ok)

        except ValueError:
            QMessageBox.information(None, '', '请选择一个有效的波特率',
                                QMessageBox.StandardButton.Ok)

    else:
        ui.ComCtrl.setText("打开串口")
        data_thread.open_flag = False
        data_thread.exit()
        open_Serial.close()

def TemOpen_clicked(): # 温度波形显示按钮
    if(ui.TemOpen.text() == "打开波形显示"):
        data_thread.draw()
        ui.TemOpen.setText("关闭波形显示")
    else:
        data.end_draw()
        ui.TemOpen.setText("打开波形显示")

def TemCtrl_clicked():
    if(ui.TemCtrl.text() == "暂停波形显示"):
        data_thread.draw_ctrl = False
        ui.TemCtrl.setText("继续波形显示")
    else:
        data_thread.draw_ctrl = True
        ui.TemCtrl.setText("暂停波形显示")

def QtEvent():
    ui.ComCtrl.clicked.connect(ComCtrl_clicked) # type: ignore
    ui.TemCtrl.clicked.connect(TemCtrl_clicked) # type: ignore
    ui.TemOpen.clicked.connect(TemOpen_clicked)

if __name__ == "__main__":
    ui = Ui_Form()
    app = QApplication(sys.argv)
    window = QWidget()
    ui.setupUi(window)

    get_serial()
    QtEvent()
    window.show()
    sys.exit(app.exec())