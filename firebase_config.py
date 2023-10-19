import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("schedule-managment-f2cf5-firebase-adminsdk-v3rzo-0734fbee96.json")
app = firebase_admin.initialize_app(cred)

firebaseConfig = {
  'apiKey': "AIzaSyBa0tmTRBtAS0VxM_ZTmdzSd-TGOZmsTE0",
  'authDomain': "schedule-managment-f2cf5.firebaseapp.com",
  'projectId': "schedule-managment-f2cf5",
  'databaseURL': "https://schedule-managment-f2cf5.firebaseio.com",
  'storageBucket': "schedule-managment-f2cf5.appspot.com",
  'messagingSenderId': "884473805272",
  'appId': "1:884473805272:web:1912144aafb99af8aa5aad"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db = firestore.client()

