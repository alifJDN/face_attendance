import cv2
import face_recognition
import numpy as np
import os
from tkinter import *
from PIL import Image, ImageTk
import SQL_Config

# Directory containing known face images
known_faces_dir = "db"  # Create this folder and add images of known people

# Lists to store known face encodings and names
known_face_encodings = []
known_face_names = []

# Load known faces from the directory
def load_known_faces():
    for filename in os.listdir(known_faces_dir):
        if filename.endswith((".jpg", ".png")):
            image_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            name = os.path.splitext(filename)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)

# Main application class
class FaceRecognitionApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Face Recognition App")
        self.window.geometry("640x540")  # Window size (adjust as needed)

        # Initialize webcam
        self.video_capture = cv2.VideoCapture(0)
        self.running = True

        # Canvas for video feed
        self.canvas = Canvas(window, width=640, height=480)
        self.canvas.pack()

        # Button below the canvas
        self.btn_toggle = Button(window, text="Stop", command=self.recognize_face)
        self.btn_toggle.pack(pady=10)

        # Load known faces
        load_known_faces()

        # Start the video update loop
        self.update_video()

    def update_video(self):
        if not self.running:
            return

        # Capture frame-by-frame
        ret, frame = self.video_capture.read()
        if not ret:
            return

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Recognize faces
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.3)
            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                print('Detected:', name)
            face_names.append(name)

        # Draw boxes and names
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Convert frame to Tkinter-compatible format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update canvas with the new frame
        self.canvas.create_image(0, 0, anchor=NW, image=imgtk)
        self.canvas.imgtk = imgtk  # Keep a reference to avoid garbage collection

        # Schedule the next update
        self.window.after(10, self.update_video)

    def toggle_video(self):
        # Toggle video on/off
        if self.running:
            self.running = False
            self.btn_toggle.config(text="Start")
        else:
            self.running = True
            self.btn_toggle.config(text="Stop")
            self.update_video()

    def on_closing(self):
        # Cleanup on window close
        self.running = False
        self.video_capture.release()
        self.window.destroy()

# Create and run the application
if __name__ == "__main__":
    root = Tk()
    app = FaceRecognitionApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Handle window close event
    root.mainloop()