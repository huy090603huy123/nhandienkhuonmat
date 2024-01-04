import cv2
import os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataset'

def check_dataset_empty(imagePaths):
    if len(imagePaths) == 0:
        print("không có ảnh nào trong thư mục dataset.")
        return True
    return False

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

    if check_dataset_empty(imagePaths):
        return None, None

    faces = []
    IDs = []
    for imagePath in imagePaths:
        faceImg = Image.open(imagePath).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        print(f"Đã thêm hình ảnh có ID: {ID}")
        IDs.append(ID)
        cv2.imshow("training", faceNp)
        cv2.waitKey(10)
    return IDs, faces

Ids, faces = getImagesAndLabels(path)

if Ids is not None:
    
    recognizer.train(faces, np.array(Ids))
    recognizer.save('recognizer/trainingData.yml')
    print("Đẫ đặt hình ảnh thành công.")
    cv2.destroyAllWindows()
