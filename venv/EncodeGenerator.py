import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import  storage
from google.cloud import storage

data = os.path.abspath(os.path.dirname(__file__)) + "/smarttttt-94151-firebase-adminsdk-v5sfa-9fbface78c.json"
cred = credentials.Certificate(data)

firebase_admin.initialize_app(cred, {
    'databaseURL': "https://smarttttt-94151-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "gs://smarttttt-94151.appspot.com"
})


# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])
    ''''
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    '''''


bucket_name='smarttttt-94151'
source_file_name='images'
destination_blob_name='test/hello.txt'

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    client = storage.Client.from_service_account_json('/smarttttt-94151-firebase-adminsdk-v5sfa-9fbface78c.json')
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name) 

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

if __name__ == '__main__':
        upload_blob(bucket_name, source_file_name, destination_blob_name)

    # print(path)
    # print(os.path.splitext(path)[0])
print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")
img = cv2.imread(os.path.join(folderPath, path))


file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")