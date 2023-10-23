import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("datas/schedule-5fac6-firebase-adminsdk-s4ppo-28b8fb6e84.json")
app = firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyBrm_j4jNNUcIi90OKgpIk-Htpyl3EbeKE",
  'authDomain': "schedule-5fac6.firebaseapp.com",
  'projectId': "schedule-5fac6",
  'storageBucket': "schedule-5fac6.appspot.com",
  'messagingSenderId': "521697645826",
  'appId': "1:521697645826:web:a9c191690392f856969e1b",
  'databaseURL': "https://schedule-5fac6.firebaseio.com"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

db = firestore.client()

