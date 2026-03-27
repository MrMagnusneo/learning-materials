import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Путь к модели
MODEL_PATH = 'blaze_face_short_range.tflite'

# Настройка опций детектора
BaseOptions = python.BaseOptions
FaceDetector = vision.FaceDetector
FaceDetectorOptions = vision.FaceDetectorOptions
VisionRunningMode = vision.RunningMode

options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    min_detection_confidence=0.5
)

# Загрузка изображения
img_path = '/home/x13/Downloads/Без имени.jpg'
img = cv2.imread(img_path)

if img is None:
    print("Ошибка: не удалось загрузить изображение")
    exit()

# Конвертация для MediaPipe
rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

# Коэффициент расширения области лица
EXPANSION_RATIO = 0.15

# Детекция лиц
with FaceDetector.create_from_options(options) as detector:
    results = detector.detect(mp_image)
    
    if results.detections:
        img_h, img_w = img.shape[:2]
        for detection in results.detections:
            bbox = detection.bounding_box
            x, y, width, height = bbox.origin_x, bbox.origin_y, bbox.width, bbox.height
            
            # Расширение области для полного закрытия лица
            expanded_x = int(x - width * EXPANSION_RATIO)
            expanded_y = int(y - height * EXPANSION_RATIO)
            expanded_width = int(width * (1 + 2 * EXPANSION_RATIO))
            expanded_height = int(height * (1 + 2 * EXPANSION_RATIO))
            
            # Ограничение границ изображения
            expanded_x = max(0, expanded_x)
            expanded_y = max(0, expanded_y)
            expanded_width = min(expanded_width, img_w - expanded_x)
            expanded_height = min(expanded_height, img_h - expanded_y)

            # Закрашивание области лица
            cv2.rectangle(img, (expanded_x, expanded_y), 
                         (expanded_x + expanded_width, expanded_y + expanded_height), 
                         (0, 0, 0), -1)

# Сохранение результата
cv2.imwrite('output.png', img)
print("Обработка завершена. Результат сохранён в output.png")

cv2.destroyAllWindows()