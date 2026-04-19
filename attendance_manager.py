import csv
import os
from datetime import datetime

file_path = "attendance/attendance.csv"

def mark_attendance(name):

    os.makedirs("attendance", exist_ok=True)

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # create file if not exists
    if not os.path.exists(file_path):
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Date", "Time"])

    # check duplicates
    already_marked = False

    try:
      with open(file_path, "r") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) >=2 and row[0] == name and row[1] == date:
                already_marked = True
                break

    except FileNotFoundError:
        name=[]

    if not already_marked:
        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, date, time])
        print(f"Attendance marked for {name}")