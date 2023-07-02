import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

cred = credentials.Certificate("face-key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-detection-9bac5-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'storageBucket': "face-detection-9bac5.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModePath = 'Resources/modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file made with pickle containing images encoded data
print("Loading Encode File ...")
file = open('EncodeFile.p', 'rb')   # Opening EncodeFile in reading mode
encodeListKnownWithIds = pickle.load(file)  # storing the data in encodeListKnownWithIds
file.close()    # close the file
encodeListKnown, studentIds = encodeListKnownWithIds    # retracting the individual elements
print(studentIds)
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    imgf = cv2.resize(img, (0, 0), None, 1.15625, 1.15625)
    # Resizing the webCamera image
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # As openCV supports BGR and face_recognition supports RGB
    # So converting the opencv image from BGR to RGB format
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[163:163 + 555, 74:74 + 740] = imgf
    imgBackground[0:0 + 788, 888:888 + 512] = imgModeList[modeType]

    if faceCurFrame:
        print("Face detected to detect !!!")
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)
            #
            if matches[matchIndex]:
                print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 74 + x1, 163 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    # cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    # cv2.imshow("Face Attendance", imgBackground)
                    # cv2.waitKey(1)
                    counter = 1
                    modeType = 1
                    # print("counter = 1 - ", counter)

        if counter != 0:

            if counter == 1:
                # print("counter = 1 - ", counter)
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # These next 3 lines of code downloads the image from cloud storage and then displays it
                # this process takes a lot of time so our display lags
                # I am using already downloaded images from the database stored in folder Images
                # Get the Image from the storage
                # blob = bucket.get_blob(f'Images/{id}.jpg')
                # array = np.frombuffer(blob.download_as_string(), np.uint8)
                # imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                imgStudent = cv2.imread(f'Images/{id}.jpg') # using images stored in folder Images
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print("Time Elapsed after last attendance = ", secondsElapsed)
                if secondsElapsed > 20:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[0:0 + 788, 888:888 + 512] = imgModeList[modeType]

            if modeType != 3:

                if 5 < counter < 8:
                    # print("5 < counter < 8 - ", counter)
                    modeType = 2

                imgBackground[0:0 + 788, 888:888 + 512] = imgModeList[modeType]

                if counter <= 5:
                    # print("counter <= 5 - ", counter)
                    cv2.putText(imgBackground, str(studentInfo['name']).upper(), (1050, 406), cv2.FONT_HERSHEY_DUPLEX, 0.7, (114, 255, 193), 1)
                    cv2.putText(imgBackground, str(studentInfo['Entry_Number']).upper(), (1142, 446), cv2.FONT_HERSHEY_DUPLEX, 0.7, (114, 255, 193), 1)
                    cv2.putText(imgBackground, str(studentInfo['Branch']).upper(), (1069, 488), cv2.FONT_HERSHEY_DUPLEX, 0.7, (114, 255, 193), 1)
                    cv2.putText(imgBackground, str(studentInfo['Degree']).upper(), (1069, 528), cv2.FONT_HERSHEY_DUPLEX, 0.7, (114, 255, 193), 1)
                    cv2.putText(imgBackground, str(studentInfo['year_of_Joining']).upper(), (1154, 568), cv2.FONT_HERSHEY_DUPLEX, 0.7, (114, 255, 193), 1)
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']).upper(), (1283, 705), cv2.FONT_HERSHEY_DUPLEX, 1, (114, 255, 193), 1)

                    # (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 0.7, 1)
                    # offset = (414 - w) // 2

                    imgBackground[95:95 + 216, 1036:1036 + 216] = imgStudent

                counter += 1

                if counter >= 8:
                    # print("counter >= 8 - ", counter)
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[0:0 + 788, 888:888 + 512] = imgModeList[modeType]
    else:
        print("No Face to detect")
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
