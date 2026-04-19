import pickle

# Open the pickle file in binary read mode
with open("encodings/face_encodings.pkl", "rb") as file:
     data = pickle.load(file),
print(data)
# write the pickle data into new txt file
with open("model_learnings.txt","w",encoding="utf-8") as f:
       f.write(str(data))


