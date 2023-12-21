import cv2
import pyodbc
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image, ImageTk
from GU import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
import subprocess
class khuonmat(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect to SQL Server
        self.conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=DESKTOP-2F3KP2O;'
            r'DATABASE=FaceRecognitionDB;'
            r'UID=khuonmat;'
            r'PWD=123456;'
        )
        try:
            self.conn = pyodbc.connect(self.conn_str)
            print("Đang kết nối tới SQL Server")
        except pyodbc.Error as ex:
            print(f"Lôi kết nối đến CSDL: {ex}")
            sys.exit(1)

        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        #url="http://172.20.10.2:4747/video" #ket noi den camera  
        #url="http://192.168.1.67:4747/video"     
        self.cam = cv2.VideoCapture(0)
        self.pushButton.clicked.connect(self.on_capture_button_click)
        
        self.xoa.clicked.connect(self.xoasql)
        self.sql.cellClicked.connect(self.cellclick)
        self.sua.clicked.connect(self.suasql)
        self.pushButton_2.clicked.connect(self.thoat)
        self.Back.clicked.connect(self.quaylai)
        self.quet.clicked.connect(self.quetmat)
        self.load1.clicked.connect(self.load)

        self.hienthi()

    def quetmat(self):         
        subprocess.run(["python", r"D:\BAP TAP Python\face1\demotraining.py"]) 

    def quaylai(self):
        self.hide()  # Hide the current window
        subprocess.run(["python", r"D:\BAP TAP Python\face1\main.py"])
        sys.exit()
    def load(self):
        self.hide()  # Hide the current window
        subprocess.run(["python", r"D:\BAP TAP Python\face1\demo.py"])
        sys.exit()

    def thoat (self):
        self.close()

    def hienthi(self):
        cursor = self.conn.cursor()
        try:
            cmd = "SELECT * FROM People"
            cursor.execute(cmd)
            rows = cursor.fetchall()
            self.sql.clearContents()
            self.sql.setRowCount(0)
            self.sql.setRowCount(len(rows))            
            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.sql.setItem(i, j, item)
        except pyodbc.Error as ex:
            print(f"Lỗi lấy dữ liệu từ cơ sở dữ liệu: {ex}")

    def Them(self, Id, Name, Age, Gender):
        cursor = self.conn.cursor()
        try:
            cmd = "SELECT * FROM People WHERE ID = ?"
            cursor.execute(cmd, (Id,))
            row = cursor.fetchone()

            if row:
                cmd = "UPDATE People SET Name = ?, Age = ?, Gender = ? WHERE ID = ?"
                cursor.execute(cmd, (Name, Age, Gender, Id))
            else:
                cmd = "INSERT INTO People(Id, Name, Age, Gender) VALUES (?, ?, ?, ?)"
                cursor.execute(cmd, (Id, Name, Age, Gender))

            self.conn.commit()
            
        except pyodbc.Error as ex:
            print(f"Lỗi CSDL: {ex}")

    def cellclick(self, row, column):
        
        id_item = self.sql.item(row, 0)
        name_item = self.sql.item(row, 1)
        age_item = self.sql.item(row, 2)
        gender_item = self.sql.item(row, 3)

        if id_item:
            self.id.setText(id_item.text())
        if name_item:
            self.hoten.setText(name_item.text())
        if age_item:
            self.tuoi.setText(age_item.text())
        if gender_item:
            if gender_item.text().lower() == 'nam':
                self.nam.setChecked(True)
            elif gender_item.text().lower() == 'nữ':
                self.nu.setChecked(True)

    def xoasql(self):
        selected_row = self.sql.currentRow()
        if selected_row >= 0:
            id_item = self.sql.item(selected_row, 0)
            if id_item:
                id = int(id_item.text())
                cursor = self.conn.cursor()
                try:
                    cmd = "DELETE FROM People WHERE ID = ?"
                    cursor.execute(cmd, (id,))
                    self.conn.commit()
                    self.hienthi()
                except pyodbc.Error as ex:
                    print(f"Lỗi Xóa dữ liệu từ cơ sở dữ liệu: {ex}")
        else:
            QMessageBox.warning(self, "Cảnh Báo", "Không Có ROW.", QMessageBox.StandardButton.Ok)  


    def suasql(self):
        id = self.id.text()
        name = self.hoten.text()
        age = self.tuoi.text()
        gender = 'Nam' if self.nam.isChecked() else 'Nữ'

        self.Them(id, name, age, gender)
        self.hienthi()

    def capture_images(self, user_id):
        sample_num = 0
        while True:         
            ret, img = self.cam.read()          
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sample_num += 1
                img_filename = f"dataset/User.{user_id}.{str(sample_num)}.jpg"
                cv2.imwrite(img_filename, gray[y:y + h, x:x + w])
                cv2.imshow('Khuôn Mặt', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sample_num > 250:
                break
        self.cam.release()
        cv2.destroyAllWindows()

    def on_capture_button_click(self):
        try:
            user_id = int(self.id.text())
            if user_id <= 0:
                raise ValueError("ID phải là số nguyên dương.")

            user_name = self.hoten.text().strip()
            if not user_name or any(char.isdigit() for char in user_name):
                raise ValueError("Tên không hợp lệ. Tên không được để trống và không được chứa chữ số.")

            user_age = int(self.tuoi.text())
            if user_age < 0:
                raise ValueError("Tuổi phải là số nguyên không âm.")

            user_gender = "Nam" if self.nam.isChecked() else "Nữ"

            self.Them(user_id, user_name, user_age, user_gender)

            self.capture_images(user_id)

            self.load()         
            self.hienthi()
        except ValueError as ve:
            
            error_message = f"Error: {ve}"
            QMessageBox.critical(self, "Error", error_message, QMessageBox.StandardButton.Ok)

        except pyodbc.Error as ex:          
            error_message = f"Lỗi: {ex}"
            QMessageBox.critical(self, "Lỗi", error_message, QMessageBox.StandardButton.Ok)

       
    def closeEvent(self, event):
        if self.conn:
            self.conn.commit()
            self.conn.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = khuonmat()
    mainWindow.show()
    sys.exit(app.exec())
