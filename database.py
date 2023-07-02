import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("face-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-detection-9bac5-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "face-detection-9bac5.appspot.com"
})

ref = db.reference('Students')
print("Updating...")
data = {
    "1177":
        {
            "name": "Himanshu Galav",
            "Entry_Number": "2021eeb1177",
            "Branch": "Electrical",
            "Degree": "Btech",
            "total_attendance": 0,
            "year_of_Joining": 2021,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1212":
        {
            "name": "Shreya Maheshwari",
            "Entry_Number": "2021eeb1212",
            "Branch": "Electrical",
            "Degree": "Btech",
            "total_attendance": 0,
            "year_of_Joining": 2021,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1220":
        {
            "name": "Tom Holland",
            "Entry_Number": "2021eeb1220",
            "Branch": "Mechanical",
            "Degree": "Mtech",
            "total_attendance": 0,
            "year_of_Joining": 2020,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1145":
        {
            "name": "Abhinav Burman",
            "Entry_Number": "2021eeb1145",
            "Branch": "Electrical",
            "Degree": "Btech",
            "total_attendance": 0,
            "year_of_Joining": 2021,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "1225":
        {
            "name": "Yash Agarwal",
            "Entry_Number": "2021eeb1225",
            "Branch": "Electrical",
            "Degree": "Btech",
            "total_attendance": 0,
            "year_of_Joining": 2021,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)

print("Updated!!!")
