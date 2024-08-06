# %% 
import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())
# %%
