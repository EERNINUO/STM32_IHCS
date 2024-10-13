from pathlib import Path
import pandas as pd
from data import Data
class File():
    def __init__(self,) -> None:
        self.dateframe:pd.DataFrame

    def tran_data(self, dat_thread:Data):
        data = {}
        data['time'] = dat_thread.time
        data['tem_channel'] = dat_thread.tem
        data['wet_channel'] = dat_thread.wet
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
