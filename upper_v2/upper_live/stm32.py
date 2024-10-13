import struct
from serial import Serial
import serial.tools.list_ports
from Ui_UI_v2 import Ui_MainWindow

byte_size = (5, 6, 7, 8)
stop_bits = (1, 1.5, 2)
parities = ['N', 'E', 'O', 'M', 'S']

class STM32(Serial):
    def __init__(self, Ui:Ui_MainWindow):
        self.Ui = Ui
        port = Ui.ComList.currentText()
        baudrate = int(self.Ui.BaudRate.currentText())
        bytesize = byte_size[self.Ui.DataBit.currentIndex()]
        stopbits = stop_bits[self.Ui.StopBit.currentIndex()]
        parity = parities[self.Ui.CaliBit.currentIndex()]

        super().__init__(port, baudrate, bytesize, parity, stopbits, timeout=0.1)
        self.collet_interval = Ui.intervalLine.text()
        
    def read_data(self) -> tuple: 
        input_dat = self.read(6)
        if input_dat != b'' and len(input_dat) == 6: # 防止输入错误数据
            re_dat = struct.unpack('BBBBH',input_dat)
            return re_dat
        else: 
            return "NULL"

    def trans_data(self, com:serial.Serial) -> tuple:
        get_dat = self.read_data()
        re_wet = 0
        re_tem = 0
        if get_dat == "NULL":
            re_tem = "NULL"
        elif get_dat == (170, 170, 170, 170, 43690) : # 0xAA * 4
            re_tem ="warning"
        elif get_dat == (187, 187, 187, 187, 48059) : # 0xBB * 4
            re_tem ="end_warning"
        else:
            re_tem = get_dat[2] + get_dat[3] * 0.1
            re_wet = get_dat[0] + get_dat[1] * 0.1
        channel1 = get_dat[4] / 4096
        # channel2 = get_dat[5] / 4096
        # channel3 = get_dat[6] / 4096
        return re_tem, re_wet, channel1#, channel2, channel3

    def send_data(self, interval_time, channel):
        out_dat = struct.pack(">HB", interval_time, channel)
        self.write(out_dat)

    def get_stm32_config(self):
        channal = 0
        if self.Ui.channel1.isChecked():
            channal += 1
        if self.Ui.channel2.isChecked():
            channal += 2
        if self.Ui.channel3.isChecked():
            channal += 4
        if self.Ui.tem_channel.isChecked():
            channal += 8
        if self.Ui.wet_channel.isChecked():
            channal += 16
        interval_time = int(self.Ui.intervalLine.text())
        return interval_time, channal