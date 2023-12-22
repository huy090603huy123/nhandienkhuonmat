import cv2
import pyodbc
import webbrowser
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-2F3KP2O;'
    r'DATABASE=Face;'
    r'UID=khuonmat;'
    r'PWD=123456;'
)
try:
    conn = pyodbc.connect(conn_str)
    print("Kết Nối Với Camera...")
except pyodbc.Error as ex:
    print(f"Lỗi DATABASE: {ex}")
    exit(1)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def recognize_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y + h, x:x + w]
        user_id, confidence = recognizer.predict(face_roi)
        if confidence < 100:  
            user_name = get_user_name(user_id)
            facebook_url = get_facebook_url(user_id)

            if facebook_url:
                webbrowser.open_new(facebook_url)
            cv2.destroyAllWindows()
            return True
    return False
def get_user_name(user_id):
    cursor = conn.cursor()
    try:
        cmd = "SELECT Name FROM People WHERE ID = ?"
        cursor.execute(cmd, (user_id,))
        row = cursor.fetchone()
        return row[0] if row else f"User {user_id}"
    except pyodbc.Error as ex:
        print(f"Lỗi không có tên người này trong CSDL: {ex}")
        return f"User {user_id}"

def get_facebook_url(user_id):
    cursor = conn.cursor()
    try:
        cmd = "SELECT FacebookURL FROM People WHERE ID = ?"
        cursor.execute(cmd, (user_id,))
        row = cursor.fetchone()
        return row[0] if row else None
    except pyodbc.Error as ex:
        print(f"Lỗi không có URL của người này trong CSDL: {ex}")
        return None

def main():
    url="http://10.15.46.101:4747/video"
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break
        if recognize_faces(frame):
            break
    cap.release()
    cv2.destroyAllWindows()
    conn.close()
if __name__ == "__main__":
    main()
