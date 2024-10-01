import struct
import serial
import serial.tools.list_ports

def read_data(com:serial.Serial): 
    input_dat = com.read(4)
    if input_dat != b'' and len(input_dat) == 4:
        re_dat = struct.unpack('I',input_dat)
        return re_dat[0]
    else: 
        return "NULL"

def trans_data(com:serial.Serial) -> tuple:
    get_dat = read_data(com)
    re_wet = 0
    re_tem = 0
    if get_dat == "NULL":
        re_tem = "NULL"
    elif get_dat == 2863311530 : # 0xAA * 4
        re_tem ="warning"
    elif get_dat == 3149642683 : # 0xBB * 4
        re_tem ="end_warning"
    else:
        re_wet_int = get_dat % 256
        get_dat >>= 8
        re_wet_flt = get_dat % 256
        get_dat >>= 8
        re_tem_int = get_dat % 256
        get_dat >>= 8
        re_tem_flt = get_dat
        re_tem = re_tem_int + re_tem_flt * 0.1
        re_wet = re_wet_int + re_wet_flt * 0.1
    return re_tem, re_wet
