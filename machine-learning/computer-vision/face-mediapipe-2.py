import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

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

EXPANSION_RATIO = 0.15

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
            img_h, img_w = frame.shape[:2]
            for detection in results.detections:
                bbox = detection.bounding_box
                x, y, width, height = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
                
                expanded_x = int(x - width * EXPANSION_RATIO)
                expanded_y = int(y - height * EXPANSION_RATIO)
                expanded_width = int(width * (1 + 2 * EXPANSION_RATIO))
                expanded_height = int(height * (1 + 2 * EXPANSION_RATIO))
                
                expanded_x = max(0, expanded_x)
                expanded_y = max(0, expanded_y)
                expanded_width = min(expanded_width, img_w - expanded_x)
                expanded_height = min(expanded_height, img_h - expanded_y)

                cv2.rectangle(frame, (expanded_x, expanded_y), (expanded_x + expanded_width, expanded_y + expanded_height), (0, 0, 0), -1)
        
        cv2.imshow('cam', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()