import face_recognition # Face detection +Encoding
import os #Handle FIles
import pickle #Save Data In binary format

dataset_path = "dataset"

known_encodings = []
known_names = []

print("Loading dataset...")
#Loop through each folder:Each person
for person_name in os.listdir(dataset_path):
    
    person_folder = os.path.join(dataset_path, person_name)
    #Goes through each image
    for image_name in os.listdir(person_folder):
        
        image_path = os.path.join(person_folder, image_name)
        #It reada Images into array
        image = face_recognition.load_image_file(image_path)
        #Detects where are the faces in the images
        face_locations = face_recognition.face_locations(image)
        #Convert each face into a 128 dmensional numerical vector
        #i.e-> face encodings
        encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in encodings:
            #Storing Encodings
            known_encodings.append(encoding)
            known_names.append(person_name)

print("Encoding completed")

data = {
    "encodings": known_encodings,
    "names": known_names
}

os.makedirs("encodings", exist_ok=True)
#It stores all data into pickle file
#face_encodings : contains @All face vectors + Correspoding names
with open("encodings/face_encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Model trained successfully!")
print("Encodings saved in encodings/face_encodings.pkl")


#We don't need to rerun this encodings once the images incoded 
##rencode only when: New Student registration ,or make any chhanges to dataseet