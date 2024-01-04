from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QApplication
import sys

from danhsach import Ui_MainWindow

class DiemDanhApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DiemDanhApp, self).__init__()
        self.setupUi(self)

        self.db = QSqlDatabase.addDatabase("QODBC")
        self.db.setDatabaseName("DRIVER={ODBC Driver 17 for SQL Server};"
                                "SERVER=DESKTOP-2F3KP2O;"
                                "DATABASE=Face1;"
                                "UID=khuonmat;"
                                "PWD=123456;")

        if not self.db.open():
            QtWidgets.QMessageBox.critical(self, "lỗi", "CSDL không vào được")
            sys.exit(1)
        self.model = QSqlTableModel()
        self.model.setTable("diemdanh")
        self.model.select()
        font = QtGui.QFont("Arial", 15)  
        self.danhsach.setFont(font)
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.green) 
        self.danhsach.setPalette(palette) 
        self.danhsach.setModel(self.model)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    diemdanh_app = DiemDanhApp()
    diemdanh_app.show()
    sys.exit(app.exec_())
