import cv2
import os
import time
# Folder to save images
import sys
name = sys.argv[1]

print("Capturing faces for:", name)
dataset_path =f"dataset/{name}"

# Create folder if it does not exist
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

# Initialize webcam
cap = cv2.VideoCapture(0)

count = 0
# max_images = 10# For auto capture
# print("Starting auto capture...")
print("Start Capturing")

# while count < max_images:
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break

    cv2.imshow("Webcam", frame)   # Show the framec

    if cv2.waitKey(1) & 0xFF == ord('c'):

          # Image filename
           img_name = os.path.join(dataset_path, f"user_{count+1}.jpg")
           # Save image
           cv2.imwrite(img_name, frame)
           print(f"Saved {img_name}")
           count += 1
###############AUTO CAPTURE#################
#Make while < max image:
    # # Show camera preview
    # cv2.imshow("Auto Capture", frame)

    # # Image filename
    # img_name = os.path.join(dataset_path, f"user_{count+1}.jpg")

    # # Save image
    # cv2.imwrite(img_name, frame)
    # print(f"Saved {img_name}")

    # count += 1

    # Wait 1 second between captures
    # time.sleep(1)
###############################################
    # Press q to stop early
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

print("Capture completed!")