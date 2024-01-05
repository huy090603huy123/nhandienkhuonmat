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
    ui.chatbox.clicked.connect(c)
    ui.thoat.clicked.connect(sys.exit)
    ui.url.clicked.connect(u)
    ui.chamcong.clicked.connect(h)
    MainWindow.show()

def x():   
    subprocess.run(["python", r"D:\BAP TAP Python\face1\demotraining.py"])

def papeGU():
    MainWindow.hide()
    subprocess.run(["python", r"D:\BAP TAP Python\face1\FB1.py"])

def y(): 
    subprocess.run(["python", r"D:\BAP TAP Python\face1\TestFaceTiLe.py"])

def c(): 
    subprocess.run(["python", r"D:\BAP TAP Python\face1\chatboxface.py"])

def u(): 
    subprocess.run(["python", r"D:\BAP TAP Python\face1\FB2.py"])

def h(): 
    subprocess.run(["python", r"D:\BAP TAP Python\face1\danhsach1.py"])


homeui()
sys.exit(app.exec_())
