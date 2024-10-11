# GNU GENERAL PUBLIC LICENSE (GPL) v3.0
# 
# Copyright (c) EERNIINUO
# which is available at https://github.com/EERNINUO/STM32_IHCS
# 
# All rights reserved.

import sys
import serial.tools
from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox, QMainWindow
from Ui_UI_v2 import Ui_MainWindow
from QtEvent import Connect

def get_serial():
    ports_list = list(serial.tools.list_ports.comports())
    for port in ports_list:
        ui.ComList.addItem(port[1][-5:-1])

if __name__ == "__main__":
    ui = Ui_MainWindow()
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui.setupUi(window)

    QTevent =  Connect(ui)
    get_serial()

    window.show()
    sys.exit(app.exec())
