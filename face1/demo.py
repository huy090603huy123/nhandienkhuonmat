from PyQt6 import QtCore, QtGui, QtWidgets
import cv2
import pyodbc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 30, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(120, 90, 321, 231))
        self.groupBox.setObjectName("groupBox")
        self.id = QtWidgets.QLineEdit(self.groupBox)
        self.id.setGeometry(QtCore.QRect(110, 30, 161, 20))
        self.id.setObjectName("id")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(40, 30, 47, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 70, 71, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(30, 110, 47, 13))
        self.label_4.setObjectName("label_4")
        self.hoten = QtWidgets.QLineEdit(self.groupBox)
        self.hoten.setGeometry(QtCore.QRect(110, 70, 161, 20))
        self.hoten.setObjectName("hoten")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(30, 150, 47, 13))
        self.label_5.setObjectName("label_5")
        self.tuoi = QtWidgets.QLineEdit(self.groupBox)
        self.tuoi.setGeometry(QtCore.QRect(110, 140, 161, 20))
        self.tuoi.setObjectName("tuoi")
        self.nam = QtWidgets.QRadioButton(self.groupBox)
        self.nam.setGeometry(QtCore.QRect(110, 110, 82, 17))
        self.nam.setObjectName("nam")
        self.nu = QtWidgets.QRadioButton(self.groupBox)
        self.nu.setGeometry(QtCore.QRect(190, 110, 82, 17))
        self.nu.setObjectName("nu")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(140, 180, 101, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect to SQL Server
        conn_str = (
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=DESKTOP-2F3KP2O;'
            r'DATABASE=FaceRecognitionDB;'
            r'UID=khuonmat;'
            r'PWD=123456;'
        )

        try:
            self.conn = pyodbc.connect(conn_str)
            print("Connected to SQL")
        except pyodbc.Error as ex:
            print(f"Error connecting to SQL: {ex}")
            exit(1)

        self.pushButton.clicked.connect(self.insertOrUpdate)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Phần Mềm Nhận Diện Khuôn Mặt"))
        self.groupBox.setTitle(_translate("MainWindow", "Thông Tin Người "))
        self.label_2.setText(_translate("MainWindow", "Nhập ID"))
        self.label_3.setText(_translate("MainWindow", "Nhập Họ Tên"))
        self.label_4.setText(_translate("MainWindow", "Giới Tính"))
        self.label_5.setText(_translate("MainWindow", "Nhập Tuổi"))
        self.nam.setText(_translate("MainWindow", "Nam"))
        self.nu.setText(_translate("MainWindow", "Nữ"))
        self.pushButton.setText(_translate("MainWindow", "Thêm"))

    def insertOrUpdate(self):
        # Get user information
        user_id, ok = QtWidgets.QInputDialog.getInt(
            self.centralwidget, 'Enter ID', 'Enter user ID (CCCD):', min=1)
        if not ok:
            return

        user_name, ok = QtWidgets.QInputDialog.getText(
            self.centralwidget, 'Enter Name', 'Enter user name:')
        if not ok:
            return

        user_age, ok = QtWidgets.QInputDialog.getInt(
            self.centralwidget, 'Enter Age', 'Enter user age:', min=0)
        if not ok:
            return

        items = ['Nam', 'Nữ']
        user_gender, ok = QtWidgets.QInputDialog.getItem(
            self.centralwidget, 'Select Gender', 'Select user gender:', items, 0, False)
        if not ok:
            return

        # Update UI for capturing
        self.label.setText("Capturing Face. Please look at the camera.")
        self.pushButton.setEnabled(False)

        # Perform face capture
        sample_num = 0
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sample_num += 1
                cv2.imwrite(f"dataset/User.{user_id}.{str(sample_num)}.jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('frame', img)

            if cv2.waitKey(100) & 0xFF == ord('q') or sample_num > 10:
                break

        cam.release()
        cv2.destroyAllWindows()

        # Update UI after capture
        self.label.setText("Face captured successfully.")
        self.pushButton.setEnabled(True)

        # Update database
        self.insertOrUpdateDatabase(user_id, user_name, user_age, user_gender)

    def insertOrUpdateDatabase(self, Id, Name, Age, Gender):
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
            print(f"Error in the database: {ex}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
