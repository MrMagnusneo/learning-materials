import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

#https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite
MODEL_PATH = 'blaze_face_short_range.tflite'

BaseOptions = python.BaseOptions
FaceDetector = vision.FaceDetector
FaceDetectorOptions = vision.FaceDetectorOptions
VisionRunningMode = vision.RunningMode

video = cv2.VideoCapture(0)

options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    min_detection_confidence=0.5
)

EXPANSION_RATIO = 0.4

with FaceDetector.create_from_options(options) as detector:
    timestamp = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        results = detector.detect_for_video(mp_image, timestamp)
        timestamp += 1
        
        if results.detections:
            for detection in results.detections:
                bbox = detection.bounding_box
                x, y, width, height = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
                cv2.rectangle(frame, (int(x), int(y)), (int(x + width), int(y + height)), (0, 0, 0), -1)
        
        cv2.imshow('cam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
