import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from threading import Thread

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Function to start the eye-controlled cursor
def start_cursor():
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)
    cap = cv2.VideoCapture(camera_index.get())

    screen_w, screen_h = pyautogui.size()

    while running:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Could not read frame.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb_frame)

        frame_h, frame_w, _ = frame.shape

        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(frame, detection)
                bbox = detection.location_data.relative_bounding_box
                eye_mid_x = int((bbox.xmin + bbox.width / 2) * frame_w)
                eye_mid_y = int((bbox.ymin + bbox.height / 2) * frame_h)

                cv2.circle(frame, (eye_mid_x, eye_mid_y), 10, (0, 255, 0), cv2.FILLED)

                screen_x = int((eye_mid_x / frame_w) * screen_w)
                screen_y = int((eye_mid_y / frame_h) * screen_h)
                pyautogui.moveTo(screen_x, screen_y)

        cv2.imshow('Eye-Controlled Cursor', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to start the eye-controlled cursor in a separate thread
def start_thread():
    global running
    running = True
    thread = Thread(target=start_cursor)
    thread.start()

# Function to stop the eye-controlled cursor
def stop_cursor():
    global running
    running = False

# Create the main window
window = tk.Tk()
window.title("Eye-Controlled Cursor")

# Dropdown to select camera index
camera_index = tk.IntVar(value=0)
camera_label = tk.Label(window, text="Select Camera Index:")
camera_label.pack()
camera_dropdown = ttk.Combobox(window, textvariable=camera_index)
camera_dropdown['values'] = (0, 1, 2, 3)
camera_dropdown.pack()

# Start and stop buttons
start_button = tk.Button(window, text="Start", command=start_thread)
start_button.pack()
stop_button = tk.Button(window, text="Stop", command=stop_cursor)
stop_button.pack()

# Run the Tkinter main loop
window.mainloop()