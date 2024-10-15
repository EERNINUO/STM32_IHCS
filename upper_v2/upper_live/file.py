from pathlib import Path
import pandas as pd
from data import Data
class File():
    def __init__(self,) -> None:
        self.dateframe:pd.DataFrame

    def tran_data(self, dat_thread:Data):
        data = {}
        data['time'] = dat_thread.time
        if dat_thread.tem_channel == True:
            data['tem_channel'] = dat_thread.tem
        if dat_thread.wet_channel == True:
            data['wet_channel'] = dat_thread.wet
        if dat_thread.channel1_flag == True:
            data['channel1'] = dat_thread.channel1
        if dat_thread.channel2_flag == True:
            data['channel2'] = dat_thread.channel2
        if dat_thread.channel3_flag == True:
            data['channel3'] = dat_thread.channel3
        self.dateframe = pd.DataFrame(data= data)

    def save_csv(self, file_path):
        path = Path(file_path)
        self.dateframe.to_csv(path)

    def save_excel(self, file_path):
        path = Path(file_path)
        self.dateframe.to_excel(path)

    def save_json(self, file_path):
        path = Path(file_path)
        self.dateframe.to_json(path)

    def open_file(self, file_path):
        path = Path(file_path[0])
        self.open_file_channel = {'tem_channel':False, 'wet_channel':False, 'channel1':False
                            , 'channel2':False, 'channel3':False}
        if (file_path[1] == "csv(*.csv)"):
            self.open_data = pd.read_csv(path)
        elif (file_path[1] == "json(*.json)"):
            self.open_data = pd.read_json(path)
        elif (file_path[1] == "xlsx(*.xlsx)"):
            self.open_data = pd.read_excel(path)
        self.file_dict = self.open_data.to_dict()
        for dict_data in self.file_dict.keys():
            if dict_data == 'tem_channel':
                self.open_file_channel['tem_channel'] = True
            elif dict_data == 'wet_channel':
                self.open_file_channel['wet_channel'] = True
            elif dict_data == 'channel1':
                self.open_file_channel['channel1'] = True
            elif dict_data == 'channel2':
                self.open_file_channel['channel2'] = True
            elif dict_data == 'channel3':
                self.open_file_channel['channel3'] = True
