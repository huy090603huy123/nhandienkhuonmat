import cv2
import face_recognition
from tkinter import filedialog
from tkinter import Tk, Button, Label, PhotoImage, Canvas

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nhận Dạng Khuôn Mặt")

        self.image_of_person = None
        self.person_face_encoding = None

        self.label = Label(root, text="Chưa chọn ảnh mẫu")
        self.label.pack()

        self.choose_image_button = Button(root, text="Chọn ảnh mẫu", command=self.choose_image)
        self.choose_image_button.pack()

        self.video_capture = cv2.VideoCapture(0)

        # Tạo khung ảnh webcam
        self.canvas = Canvas(root, width=640, height=480)
        self.canvas.pack()

        # Thực hiện cập nhật video từ webcam
        self.update_video()

    def choose_image(self):
        image_path = filedialog.askopenfilename(title="Chọn ảnh mẫu", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if image_path:
            self.image_of_person = face_recognition.load_image_file(image_path)
            self.person_face_encoding = face_recognition.face_encodings(self.image_of_person)[0]
            self.label.config(text="Đã chọn ảnh mẫu")

    def update_video(self):
        _, frame = self.video_capture.read()
        frame = cv2.resize(frame, (640, 480))
        # Tìm kiếm khuôn mặt trong frame
        face_locations = face_recognition.face_locations(frame)
        if len(face_locations) > 0 and self.person_face_encoding is not None:
            face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
            match_percentage = face_recognition.face_distance([self.person_face_encoding], face_encoding)
            match_percentage = round((1 - match_percentage[0]) * 100, 2)
            self.label.config(text=f"Tỉ Lệ Giống: {match_percentage}%")

        # Hiển thị frame lên canvas
        self.photo = self.convert_frame_to_photo(frame)
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)

        # Lặp lại hàm này mỗi 10 milliseconds
        self.root.after(10, self.update_video)


    def convert_frame_to_photo(self, frame):
        # Chuyển đổi frame thành đối tượng PhotoImage
        return PhotoImage(data=cv2.imencode('.ppm', frame)[1].tobytes())



if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
