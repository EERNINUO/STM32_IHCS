import time
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from Ui_UI_v1 import Ui_Form
import draw
import stm32

class Data(QThread):
    warning = pyqtSignal()
    def __init__(self, com, Ui:Ui_Form):
        super().__init__()
        self.com = com
        self.ui = Ui
        self.open_flag = True
        self.time = []
        self.tem = []
        self.wet = []

    def run(self):
        st_time = time.time()
        while self.open_flag:
            try:
                tem, wet = stm32.trans_data(self.com)
                if type(tem) == str:
                    if tem == 'NULL':
                        continue
                    elif tem == 'warning':
                        self.ui.GasLine.setText("含量超标")
                        self.warning.emit()
                    elif tem == 'end_warning':
                        self.ui.GasLine.setText("正常")
                else:
                    self.tem.append(tem)
                    self.wet.append(wet)
                    self.time.append(time.time() - st_time)
                    self.ui.TemLine.setText(str(tem))
                    self.ui.WetLine.setText(str(wet))
            except TypeError:
                break
