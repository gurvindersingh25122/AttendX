# import cv2
# import face_recognition
# import pickle
# import numpy as np
# from sklearn.neighbors import KNeighborsClassifier
# from attendance_manager import mark_attendance

# # Load trained encodings
# with open("encodings/face_encodings.pkl", "rb") as f:
#     data = pickle.load(f)

# X = data["encodings"]
# y = data["names"]

# # Train KNN
# knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
# knn.fit(X, y)

# print("KNN model ready")

# video = cv2.VideoCapture(0)

# #TO remember which person is present today
# framecount=0
# marked_people=set()
# while True:

#     ret, frame = video.read()
#     #IF camera fails
#     if not ret:
#         print("failed to grab frame.camera error")
#         break

#     # framecount+=1
#     # if framecount % 3 != 0:
#     #     cv2.imshow("Smart Attendance System", frame)
#     #     if cv2.waitKey(1) & 0xFF == ord("q"):
#     #         break
#     #     continue

#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     face_locations = face_recognition.face_locations(rgb)
#     face_encodings = face_recognition.face_encodings(rgb, face_locations)

#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

#         distances, indices = knn.kneighbors([face_encoding], n_neighbors=1)
#         distance = distances[0][0]


#         if distance < 0.45:
#             name = knn.predict([face_encoding])[0]

#             if name not in marked_people:
#               print("Recognized",name)
#               mark_attendance(name)
#               marked_people.add(name)
#         else:
#             name = "Unknown"

            
#         #Draw box
#         cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)

#         confidence = round((1-distance)*100,2)
#         label = f"{name} ({confidence}%)"
#         cv2.putText(frame,label,(left,top-10),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.8,(0,255,0),2)

#     cv2.imshow("Smart Attendance System", frame)

#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# video.release()
# cv2.destroyAllWindows()

######Without KNN###############

import cv2
import face_recognition
import pickle
import numpy as np
import os
import time
from datetime import datetime, date
from attendance_manager import mark_attendance

# ==============================
# LOAD ENCODINGS
# ==============================
with open("encodings/face_encodings.pkl", "rb") as f:
    data = pickle.load(f)

known_encodings = data["encodings"]
known_names = data["names"]

print("Encodings loaded successfully")

# ==============================
# START CAMERA (optimized)
# ==============================
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # reduce lag

# ==============================
# VARIABLES FOR PERFORMANCE
# ==============================
process_this_frame = True   # frame skipping toggle
marked_people = {}         # store last marked time
COOLDOWN = 60              # seconds before re-marking same person

last_date = date.today()   # for daily reset

print("Starting camera... Press 'q' to quit")

# ==============================
# MAIN LOOP
# ==============================

while True:

    ret, frame = video.read()

    if not ret:
        print("Camera error")
        break

    # ==============================
    # DAILY RESET (important)
    # ==============================
    if date.today() != last_date:
        marked_people.clear()
        last_date = date.today()
        print("New day → attendance reset")

    # ==============================
    # PROCESS EVERY ALTERNATE FRAME
    # ==============================
    # process_this_frame = not process_this_frame

    if not process_this_frame:
        cv2.imshow("Smart Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        continue

    # ==============================
    # RESIZE FRAME (MAJOR SPEED BOOST)
    # ==============================
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert BGR → RGB
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # ==============================
    # FACE DETECTION (FAST MODEL)
    # ==============================
    face_locations = face_recognition.face_locations(rgb_small, model="hog")

    # ==============================
    # FACE ENCODING
    # ==============================
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    # ==============================
    # LOOP THROUGH FACES
    # ==============================
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        # ==============================
        # COMPARE FACES (NO KNN → FASTER)
        # ==============================
        matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.45)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)

        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]
            distance = face_distances[best_match_index]
        else:
            name = "Unknown"
            distance = 1.0

        # ==============================
        # SCALE BACK FACE LOCATION
        # ==============================
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # ==============================
        # ATTENDANCE WITH COOLDOWN
        # ========================q======
        current_time = time.time()

        if name != "Unknown":
            if name not in marked_people or current_time - marked_people[name] > COOLDOWN:
                print("Recognized:", name)
                mark_attendance(name)
                marked_people[name] = current_time

        # ==============================
        # DRAW BOX & LABEL
        # ==============================
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        confidence = round((1 - distance) * 100, 2)
        label = f"{name} ({confidence}%)"

        cv2.putText(frame, label, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (0, 255, 0), 2)

    # ==============================
    # DISPLAY OUTPUT
    # ==============================
    cv2.imshow("Smart Attendance System", frame)

    # PRESS Q TO EXIT
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# ==============================
# CLEANUP
# ==============================
video.release()
cv2.destroyAllWindows()