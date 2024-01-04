import cv2
import os

# Directory containing images
directory = r'D:\BAP TAP Python\dataset\user'

# Initialize variables
num_images = 0
num_faces = 0
image_paths = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.png'):
        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Read the image
        image = cv2.imread(file_path)

        # Check if the image is not None
        if image is not None:
            # Increment the number of images
            num_images += 1

            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Detect faces in the image
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            # Increment the number of faces
            num_faces += len(faces)

            # Store the image path
            image_paths.append(file_path)

        else:
            print(f"Error processing image {file_path}")

# Print the results
print(f"Number of images: {num_images}")
print(f"Number of faces: {num_faces}")
print("Image paths:", image_paths)
