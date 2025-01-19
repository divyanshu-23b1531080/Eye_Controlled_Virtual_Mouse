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
    # Initialize face detection
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)
    
    # Select the camera based on the dropdown selection
    cap = cv2.VideoCapture(camera_index.get())

    # Get screen dimensions
    screen_w, screen_h = pyautogui.size()

    # Continue running while the global 'running' flag is True
    while running:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            # Show error message if frame reading fails
            messagebox.showerror("Error", "Could not read frame.")
            break

        # Flip the frame horizontally for a mirror effect
        frame = cv2.flip(frame, 1)
        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Process the frame with face detection
        results = face_detection.process(rgb_frame)

        # Get the frame dimensions
        frame_h, frame_w, _ = frame.shape

        if results.detections:
            # Iterate through detected faces
            for detection in results.detections:
                # Draw detection landmarks on the frame
                mp_drawing.draw_detection(frame, detection)
                # Get bounding box of the detected face
                bbox = detection.location_data.relative_bounding_box
                eye_mid_x = int((bbox.xmin + bbox.width / 2) * frame_w)
                eye_mid_y = int((bbox.ymin + bbox.height / 2) * frame_h)

                # Draw a circle at the middle of the bounding box
                cv2.circle(frame, (eye_mid_x, eye_mid_y), 10, (0, 255, 0), cv2.FILLED)

                # Map eye position to screen coordinates
                screen_x = int((eye_mid_x / frame_w) * screen_w)
                screen_y = int((eye_mid_y / frame_h) * screen_h)
                # Move the cursor to the calculated screen coordinates
                pyautogui.moveTo(screen_x, screen_y)

        # Display the frame with detections
        cv2.imshow('Eye-Controlled Cursor', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Break the loop if 'q' is pressed
            break

    # Release the camera and close all OpenCV windows
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

# Create the main window using Tkinter
window = tk.Tk()
window.title("Eye-Controlled Cursor")

# Create and pack the camera index selection label and dropdown
camera_index = tk.IntVar(value=0)
camera_label = tk.Label(window, text="Select Camera Index:")
camera_label.pack()
camera_dropdown = ttk.Combobox(window, textvariable=camera_index)
camera_dropdown['values'] = (0, 1, 2, 3)
camera_dropdown.pack()

# Create and pack the start and stop buttons
start_button = tk.Button(window, text="Start", command=start_thread)
start_button.pack()
stop_button = tk.Button(window, text="Stop", command=stop_cursor)
stop_button.pack()

# Run the Tkinter main loop
window.mainloop()
