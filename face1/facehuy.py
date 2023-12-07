import cv2
import pyodbc

# Connect to SQL Server
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=DESKTOP-2F3KP2O;'
    r'DATABASE=FaceRecognitionDB;'
    r'UID=khuonmat;'
    r'PWD=123456;'
)

try:
    conn = pyodbc.connect(conn_str)
    print("Đang kết nối SQL")
except pyodbc.Error as ex:
    print(f"Lỗi Kết Nối SQL: {ex}")
    exit(1)

detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)


def insertOrUpdate(Id, Name, Age, Gender):
    cursor = conn.cursor()
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

        conn.commit()
    except pyodbc.Error as ex:
        print(f"Lỗi Trong CSDL (database): {ex}")

while True:
    try:
        user_id = int(input('Hãy nhập địa chỉ id(CCCD): '))
        if user_id <= 0:
            raise ValueError("ID phải là số nguyên dương.")
        break
    except ValueError as ve:
        print(f"Lỗi: {ve}")

while True:
    user_name = input('Hãy nhập Họ Tên: ')
    if user_name.strip() and not any(char.isdigit() for char in user_name):
        break
    else:
        print("Tên không được để trống và không chứa số.")

while True:
    try:
        user_age = int(input('Hãy nhập tuổi: '))
        if user_age < 0:
            raise ValueError("Vui lòng nhập tuổi là một số nguyên không âm.")
        break
    except ValueError as ve:
        print(f"Lỗi: {ve}")

while True:
    user_gender = input('Hãy nhập giới tính (Nam/Nữ): ')
    if user_gender.lower() in ['nam', 'nu']:
        break
    else:
        print("Giới tính không hợp lệ. Hãy nhập 'Nam' hoặc 'Nữ'.")

insertOrUpdate(user_id, user_name, user_age, user_gender)

sampleNum = 0
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        sampleNum += 1
        cv2.imwrite(f"dataset/User.{user_id}.{str(sampleNum)}.jpg", gray[y:y + h, x:x + w])
        cv2.imshow('frame', img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    elif sampleNum > 10:
        break

cam.release()
cv2.destroyAllWindows()
conn.close()
