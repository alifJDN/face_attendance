import cv2
import os
import face_recognition

face_classifier = cv2.CascadeClassifier("face_ref_alt.xml")

video_capture = cv2.VideoCapture(0)

if face_classifier.empty():
    print("Error: Could not load Haar cascade classifier")
    exit()


#check for 
known_face_encodings = []
known_face_names = []

face_sample_dir = "face_sample"

for filename in os.listdir(face_sample_dir):
    if filename.endswith((".jpg",".jpeg",".png")):
        img_path = os.path.join(face_sample_dir,filename)
        face_encoding = face_recognition.load_image_file(img_path)
        known_face_encodings.append(face_encoding)
        known_face_names.append(os.path.splitext(filename[0]))

video_capture = cv2.VideoCapture(0)

def detect_and_recognize_face(frame):
    #convert the face to grayscale
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40,40))
    rgb_frame = frame[:, :, ::-1]

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = face_distances.argmin()
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        face_names.append(name)

    for (x, y, w, h), name in zip(faces, face_names):
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 4)
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return  frame



while True:

    result, video_frame = video_capture.read()
    if result is False:
        break

    video_frame = detect_and_recognize_face(video_frame)

    cv2.imshow("faceDetection project", video_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    video_capture.release()
cv2.destroyAllWindows()