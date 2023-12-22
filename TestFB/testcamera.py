import cv2
import pyodbc

# Database connection parameters
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-2F3KP2O;'
    r'DATABASE=Face;'
    r'UID=khuonmat;'
    r'PWD=123456;'
)

# Connect to the database
try:
    conn = pyodbc.connect(conn_str)
    print("Connected to SQL Server")
except pyodbc.Error as ex:
    print(f"Error connecting to the database: {ex}")
    exit(1)

# Load face recognizer model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('recognizer/trainingData.yml')

# Load face detector
detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def recognize_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_roi = gray[y:y + h, x:x + w]
        user_id, confidence = recognizer.predict(face_roi)

        if confidence < 100:  # Adjust confidence threshold as needed
            user_name = get_user_name(user_id)
            print(f"Recognized: {user_name}, Confidence: {confidence}%")
        else:
            print("Unknown face")

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return frame

def get_user_name(user_id):
    cursor = conn.cursor()
    try:
        cmd = "SELECT Name FROM People WHERE ID = ?"
        cursor.execute(cmd, (user_id,))
        row = cursor.fetchone()
        return row[0] if row else f"User {user_id}"
    except pyodbc.Error as ex:
        print(f"Error retrieving user name from the database: {ex}")
        return f"User {user_id}"

def main():
    cap = cv2.VideoCapture(0)  # Use camera index 0 (default) or adjust it as needed

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        frame = recognize_faces(frame)
        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    conn.close()

if __name__ == "__main__":
    main()
