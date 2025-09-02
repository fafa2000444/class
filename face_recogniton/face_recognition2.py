import cv2
import numpy as np
from insightface.app import FaceAnalysis
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle
import tkinter as tk
from tkinter import simpledialog

# ---- CONFIG ----
KNOWN_FACES_FILE = "known_faces.pkl"
SIMILARITY_THRESHOLD = 0.5  # lower = stricter (0.4–0.6 works well)

# ---- Initialize FaceAnalysis (CPU only) ----
app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

# ---- Load known faces if they exist ----
if os.path.exists(KNOWN_FACES_FILE):
    with open(KNOWN_FACES_FILE, 'rb') as f:
        known_faces = pickle.load(f)
else:
    known_faces = {}  # name -> embedding

# ---- Function to register a new face ----
def register_face(frame):
    # Create a simple dialog to enter the name
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    name = simpledialog.askstring("Input", "Enter name for registration:")
    root.destroy()  # Close the dialog window

    if name:
        faces = app.get(frame)
        if faces:
            embedding = faces[0].embedding
            known_faces[name] = embedding
            with open(KNOWN_FACES_FILE, 'wb') as f:
                pickle.dump(known_faces, f)
            print(f"[INFO] Registered face for: {name}")
        else:
            print("[WARN] No face detected. Try again.")

# ---- Function to recognize a face ----
def recognize_face(face_embedding):
    if not known_faces:
        return "Unknown"

    names = list(known_faces.keys())
    embeddings = np.array(list(known_faces.values()))

    sims = cosine_similarity([face_embedding], embeddings)[0]
    best_idx = np.argmax(sims)
    if sims[best_idx] >= SIMILARITY_THRESHOLD:
        return names[best_idx]
    return "Unknown"

# ---- Webcam Loop ----
cap = cv2.VideoCapture(0)
print("[INFO] Press 'r' to register your face, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = app.get(frame)

    for face in faces:
        box = face.bbox.astype(int)
        name = recognize_face(face.embedding)

        # Draw box and name
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        cv2.putText(frame, name, (box[0], box[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Face Recognition", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('r'):
        register_face(frame)

cap.release()
cv2.destroyAllWindows()
