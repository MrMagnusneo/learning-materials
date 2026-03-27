import cv2

video = cv2.VideoCapture(0)
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

while True:
    ret, frame = video.read()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, 1.2, 5)
    for x, y, width, height in faces:
        cv2.rectangle(frame, (x, y), (x + width, y + height), color=(0, 0, 0), thickness=-1)
    cv2.imshow('cam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
