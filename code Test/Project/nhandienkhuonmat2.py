import cv2
import os
import pyodbc

# Initialize the SQL Server connection
conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};' \
           'Server=DESKTOP-2F3KP2O;' \
           'Database=FaceRecognitionDB;' \
           'UID=khuonmat;' \
           'PWD=123456;'

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Load the Haarcascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the webcam
cap = cv2.VideoCapture(0)

# Create a folder to store user images
user_folder = 'dataset/user'
if not os.path.exists(user_folder):
    os.makedirs(user_folder)

# Number of images to capture for each person
num_images_per_person = 200

while True:
    # Insert information into the People table
    person_id = int(input("Enter the person's ID (0 to exit): "))
    if person_id == 0:
        break

    name = input("Enter the person's name: ")
    age = int(input("Enter the person's age: "))
    gender = input("Enter the person's gender: ")

    query = "INSERT INTO People (ID, Name, Age, Gender) VALUES (?, ?, ?, ?)"
    cursor.execute(query, person_id, name, age, gender)
    conn.commit()

    # Capture 200 images for the current person
    image_counter = 0
    capture_images = True 
    while image_counter < num_images_per_person and capture_images:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face_roi = frame[y:y + h, x:x + w]
            img_name = f"{user_folder}/user_{person_id}_{image_counter}.png"
            cv2.imwrite(img_name, face_roi)
            print(f"Captured image: {img_name}")

            image_counter += 1

            if image_counter == num_images_per_person:
                print(f"Captured {num_images_per_person} images for person {person_id}.")
                capture_images = False

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    print(f"Information and images for person {person_id} captured successfully.")
# Release resources
conn.close()
cap.release()
cv2.destroyAllWindows()

