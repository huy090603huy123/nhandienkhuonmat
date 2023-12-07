import cv2
import mediapipe as mp

# Khởi tạo giải pháp MediaPipe Hands
mp_hands = mp.solutions.hands.Hands()

# Khởi tạo cửa sổ video
cap = cv2.VideoCapture(0)

while True:
    # Lấy khung hình từ camera
    ret, frame = cap.read()

    # Xử lý khung hình
    frame = cv2.flip(frame, 1)
    results = mp_hands.process(frame)

    # Vẽ các điểm quan trọng của bàn tay
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                x, y = landmark.x, landmark.y
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)

    # Đếm số ngón tay
    num_fingers = 0
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for finger_tip in [hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP],
                               hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP],
                               hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP],
                               hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_FINGER_TIP]]:
                if finger_tip.x != -1:
                    num_fingers += 1

    # Hiển thị số ngón tay trên màn hình
    cv2.putText(frame, str(num_fingers), (10, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Hiển thị khung hình
    cv2.imshow("MediaPipe Hands", frame)

    # Bắt đầu lại vòng lặp nếu người dùng nhấn phím Esc
 
