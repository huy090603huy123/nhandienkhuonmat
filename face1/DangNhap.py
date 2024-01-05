from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from login import Ui_MainWindow
import subprocess
import sys
import cv2
class DangNhap(QtWidgets.QMainWindow):
    def __init__(self):
        super(DangNhap, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.cam = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("recognizer/trainingData.yml")
        self.ui.quetmat.clicked.connect(self.login_process)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout_handler)
    def capture_frame(self):
        ret, img = self.cam.read()             
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        return gray
        
    def login_process(self):   
        print("Vui Lòng Đợi Vài Phút Để Hệ Thống Quét")
        self.timer.start(5000) 
        gray = self.capture_frame()
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)     
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            user_id, conf = self.recognizer.predict(roi_gray)
            if conf < 60:           
                subprocess.Popen(["python", r"D:\BAP TAP Python\face1\main.py"], creationflags=subprocess.CREATE_NO_WINDOW)              
                self.close_program()            
                return
            else:
                QMessageBox.warning(self, "Lỗi", "Người Này Không Có trong Hệ Thống Dữ Liệu Để Đăng Nhập", QMessageBox.Ok)
    def closeEvent(self, event):
        if self.cam.isOpened():
            self.cam.release()
        event.accept()
    def timeout_handler(self):
        self.timer.stop()
        QMessageBox.warning(self, "Timeout", "Quét mặt đã quá thời gian. Vui lòng nhấn lại nút quét mặt.", QMessageBox.Ok)
       
    def close_program(self):
       QCoreApplication.quit()
if __name__ == "__main__":
    app = QApplication([])
    dangnhap_window = DangNhap()
    dangnhap_window.show()
    sys.exit(app.exec_())