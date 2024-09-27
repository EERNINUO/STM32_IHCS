import time
import Data
import stm32

x = []
y = []
st_time = time.time()

if __name__ == "__main__":
    My_stm32 = stm32.open_Serial()
    while True:
        try:
            data = stm32.read_ushort_data(My_stm32)
            if (data == 'NULL'):
                continue
            y.append(data[0])
            x.append(time.time() - st_time)
            Data.update_show(x,y)
        except KeyboardInterrupt:
            print("Do you want to exit?")
            print("1. Yes\n2. No")
            if (input("Please input 1 or 2: ") == "1"):
                break
            else:
                pass
    
    stm32.close_Serial(My_stm32)
