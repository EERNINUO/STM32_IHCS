from Ui_UI_v2 import Ui_MainWindow
import serial.serialutil
import data
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from stm32 import STM32
from file import File

class Connect():
    def __init__(self, Ui: Ui_MainWindow, main_window) -> None:
        self.Ui = Ui
        self.main_window = main_window
        self.open_serial: STM32 # 被打开的串口
        self.data_thread: data.Data #新的线程
        self.file = File()

        self.Ui.ComCtrl.clicked.connect(self.ComCtrl_clicked)
        self.Ui.TemCtrl.clicked.connect(self.TemCtrl_clicked)
        self.Ui.TemOpen.clicked.connect(self.TemOpen_clicked)
        self.Ui.collet_ctrl.clicked.connect(self.collet_ctrl)

        self.Ui.save.triggered.connect(self.save_file)
        self.Ui.open.triggered.connect(self.open_file)

    def ComCtrl_clicked(self): # 打开串口按钮
        if(self.Ui.ComCtrl.text() == "打开串口"):
            try:
                # 打开一个串口
                self.open_serial = STM32(self.Ui)
                self.Ui.ComCtrl.setText("关闭串口")
                
            #检测错误输入
            except serial.serialutil.SerialException:
                QMessageBox.information(None, '', '请选择一个串口',
                                    QMessageBox.StandardButton.Ok)
            except ValueError:
                QMessageBox.information(None, '', '请选择一个有效的波特率',
                                    QMessageBox.StandardButton.Ok)

        else:
            if self.Ui.collet_ctrl.text() == "停止采集":
                self.collet_ctrl()
            self.Ui.ComCtrl.setText("打开串口")
            self.open_serial.close()  # 关闭串口

    def TemOpen_clicked(self): # 波形显示按钮
        if(self.Ui.TemOpen.text() == "打开波形显示"):
            self.Ui.FPSLine.setReadOnly(True)
            self.Ui.widget.paint.start_my_draw(self.Ui, self.data_thread)
            self.Ui.TemOpen.setText("关闭波形显示")
        else: 
            if self.Ui.TemCtrl.text() == "暂停波形显示":
                self.TemCtrl_clicked()
            self.Ui.widget.paint.end_draw()
            self.Ui.TemOpen.setText("打开波形显示")
            self.Ui.FPSLine.setReadOnly(False)

    def TemCtrl_clicked(self):      # 
        if(self.Ui.TemCtrl.text() == "暂停波形显示"):
            self.Ui.widget.paint.timer.stop()
            self.Ui.TemCtrl.setText("继续波形显示")
        else:
            self.Ui.widget.paint.timer.start(100)
            self.Ui.TemCtrl.setText("暂停波形显示")

    def collet_ctrl(self):    # 采集控制  
        if (self.Ui.collet_ctrl.text() == "开始采集"):
            self.Ui.intervalLine.setReadOnly(True)
            interval_time, channal = self.open_serial.get_stm32_config()
            self.open_serial.send_data(interval_time, channal)
            self.data_thread = data.Data(self.open_serial, self.Ui)    # 创建读取数据的线程
            self.data_thread.start()     # 启动线程
            self.data_thread.warning.connect(lambda: 
                        QMessageBox.warning(None, '警告', 
                        '可燃气体含量超标', QMessageBox.StandardButton.Ok))
            self.Ui.collet_ctrl.setText("停止采集")
        else:
            if self.Ui.TemOpen.text() == "关闭波形显示":
                self.TemOpen_clicked()
            self.data_thread.open_flag = False
            self.data_thread.exit()   # 退出线程
            self.Ui.collet_ctrl.setText("开始采集")
            self.Ui.intervalLine.setReadOnly(False)


    def save_file(self):
        try:
            self.file.tran_data(self.data_thread)
            file = QFileDialog.getSaveFileName(self.main_window, "保存文件", "./", "csv(*.csv);;json(*.json);;xlsx(*.xlsx)")
            if (file[1] == "csv(*.csv)"):
                self.file.save_csv(file[0])
            elif (file[1] == "json(*.json)"):
                self.file.save_json(file[0])
            elif (file[1] == "xlsx(*.xlsx)"):
                self.file.save_excel(file[0])

        except PermissionError:
            pass

        except AttributeError:
            QMessageBox.critical(None, "错误", "无可以保存的数据", QMessageBox.StandardButton.Ok)

    def open_file(self):
        try:
            file = QFileDialog.getOpenFileName(self.main_window, "打开文件", "./", "csv(*.csv);;json(*.json);;xlsx(*.xlsx)")
            self.file.open_file(file)
            self.Ui.widget.paint.draw_open_file(self.file)
        except PermissionError:
            pass