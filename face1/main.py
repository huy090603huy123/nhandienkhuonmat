from PyQt5 import QtWidgets
from GUI import Ui_MainWindow
import subprocess
import sys

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

def homeui():
    ui.P1.clicked.connect(papeGU)
    ui.P2.clicked.connect(x)
    ui.camera.clicked.connect(y)
    ui.thoat.clicked.connect(sys.exit)
    MainWindow.show()

def x():   
    subprocess.run(["python", r"D:\BAP TAP Python\face1\demotraining.py"])

def papeGU():
    MainWindow.hide()
    subprocess.run(["python", r"D:\BAP TAP Python\face1\demo.py"])

def y(): 
    subprocess.run(["python", r"D:\BAP TAP Python\face1\nhandienkhuonmat.py"])


homeui()
sys.exit(app.exec_())
