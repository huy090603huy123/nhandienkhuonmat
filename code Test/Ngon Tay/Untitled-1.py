import cv2
import os
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

finger_images_dir = 'Fingers'
finger_images = [cv2.imread(os.path.join(finger_images_dir, f'{i}.png')) for i in range(6)]
while cap.isOpened():
    ret, rgb_frame = cap.read()
    if not ret:
        break
    rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)


    count = 0
    if results.multi_hand_landmarks:
        myHand = []
        count = 0
        for idx, hand in enumerate(results.multi_hand_landmarks):
          #  mp_drawing.draw_landmarks(rgb_frame, hand, mp_hands.HAND_CONNECTIONS)

            for landmark in hand.landmark:
                id = landmark.x
                lm = landmark
                h, w, _ = rgb_frame.shape
                myHand.append([int(lm.x * w), int(lm.y * h)])  # x= 0 , y= 1
            if len(myHand) >= 21:
                if myHand[4][1] < myHand[2][1] and myHand[4][0] > myHand[2][0]:
                    count = count + 1
                if myHand[8][1] < myHand[5][1]:
                    count = count + 1

                if myHand[12][1] < myHand[9][1]:
                    count = count + 1

                if myHand[16][1] < myHand[13][1]:
                    count = count + 1
                if myHand[20][1] < myHand[17][1]:
                   count = count + 1             
      
        cv2.putText(rgb_frame, f"Fingers: {count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        if count < len(finger_images):
            cv2.imshow('Finger Image', finger_images[count])


    cv2.imshow('Finger Detection', rgb_frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()