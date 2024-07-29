import cv2

# Constants
FACE_DETECTOR_XML = "face_ref_alt.xml"
TEMPLATE_IMAGE_PATH = "face_sample/alif.jpg"
TEMPLATE_IMAGE_GRAYSCALE = cv2.imread(TEMPLATE_IMAGE_PATH, 0)
MIN_FACE_SIZE = (100, 100)
SCALE_FACTOR = 1.1
ACCURACY_ESTIMATE = 0.8

face_detector = cv2.CascadeClassifier(FACE_DETECTOR_XML)
camera = cv2.VideoCapture(0)

def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, scaleFactor=SCALE_FACTOR, minSize=MIN_FACE_SIZE)
    return faces

def draw_face_box(frame):
    for x, y, w, h in detect_faces(frame):
        detection_status = None
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
        accuracy_text = f"Accuracy: {ACCURACY_ESTIMATE:.2f}"
        name_text = 'HUMAN BEING'
        face_region = gray[y:y+h, x:x+w]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, accuracy_text, (x + w + 10, y + h - 5), font, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, name_text, (x + w + 10, y + h - 30), font, 0.7, (0, 255, 0), 2)
        # cv2.matchTemplate(face_region, TEMPLATE_IMAGE_PATH, cv2.TM_SQDIFF)
        # if res:
        #     detection_status="detected"
        # else:
        #     detection_status="not deteccted"
        # cv2.putText(frame, detection_status, (x + w + 10, y + h - 50), font, 0.7, (0, 255, 0), 2)

def close_windows():
    camera.release()
    cv2.destroyAllWindows()
    exit()

def main():
    while True:
        _, frame = camera.read()
        draw_face_box(frame)
        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            close_windows()

if __name__ == '__main__':
    main()