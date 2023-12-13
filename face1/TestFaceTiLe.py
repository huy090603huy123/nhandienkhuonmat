import cv2
import numpy as np
import pyodbc

class FaceRecognizer:
    def __init__(self, database_config, recognizer_path):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read(recognizer_path)
        self.fontface = cv2.FONT_HERSHEY_SIMPLEX
        self.fontscale = 1
        self.fontcolor = (203, 23, 252)
        self.fontface = cv2.FONT_HERSHEY_DUPLEX
        # Connect to SQL Server
        self.conn_str = (
            f"DRIVER={database_config['driver']};"
            f"SERVER={database_config['server']};"
            f"DATABASE={database_config['database']};"
            f"UID={database_config['uid']};"
            f"PWD={database_config['pwd']};"
        )
        
        try:
            self.conn = pyodbc.connect(self.conn_str)
            print("Đang Kết nối Với CSDL")
            self.cursor = self.conn.cursor()
        except pyodbc.Error as ex:
            print(f"Lỗi CSDL: {ex}")
            exit(1)

    def get_profile(self, user_id):
        cmd = "SELECT * FROM People WHERE ID = ?"
        self.cursor.execute(cmd, (user_id,))
        return self.cursor.fetchone()

    def recognize_faces(self):
        cam = cv2.VideoCapture(0)
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                user_id, conf = self.recognizer.predict(gray[y:y + h, x:x + w])
                profile = self.get_profile(user_id)                
                accuracy_threshold = 60  
                if conf < accuracy_threshold and profile:
                    cv2.putText(img, "Ten: " + str(profile[1]), (x, y + h + 30), self.fontface, self.fontscale,
                                self.fontcolor, 2)
                    cv2.putText(img, "Tuoi: " + str(profile[2]), (x, y + h + 60), self.fontface, self.fontscale,
                                self.fontcolor, 2)
                    cv2.putText(img, "Gioi Tinh: " + str(profile[3]), (x, y + h + 90), self.fontface, self.fontscale,
                                self.fontcolor, 2)
                    cv2.putText(img, f"Ti Le Giong: {100 - conf:.2f}%", (x, y - 10), self.fontface, self.fontscale,
                                self.fontcolor, 2)
                else:
                    cv2.putText(img, "NO FACE", (x, y + h + 30), self.fontface, self.fontscale,
                                self.fontcolor, 2)
                    cv2.putText(img, f"Ti Le Giong: {100 - conf:.2f}%", (x, y - 10), self.fontface, self.fontscale,
                                self.fontcolor, 2)
            cv2.putText(img, "Press 'Q' to exit", (10, 20), self.fontface, self.fontscale,
                        self.fontcolor, 2)
            cv2.imshow('CAMERA AN NINH', img)
            if cv2.waitKey(1) == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()
        self.conn.close()

if __name__ == "__main__":
    database_config = {
        'driver': 'ODBC Driver 17 for SQL Server',
        'server': 'DESKTOP-2F3KP2O',
        'database': 'FaceRecognitionDB',
        'uid': 'khuonmat',
        'pwd': '123456'
    }

    recognizer_path = "recognizer\\trainingData.yml"
    face_recognizer = FaceRecognizer(database_config, recognizer_path)
    face_recognizer.recognize_faces()
