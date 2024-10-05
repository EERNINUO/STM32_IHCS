import struct
import serial
import serial.tools.list_ports

def read_data(com:serial.Serial) -> tuple: 
    input_dat = com.read(6)
    if input_dat != b'' and len(input_dat) == 6: # 防止输入错误数据
        re_dat = struct.unpack('BBBBH',input_dat)
        return re_dat
    else: 
        return "NULL"

def trans_data(com:serial.Serial) -> tuple:
    get_dat = read_data(com)
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
    return re_tem, re_wet
