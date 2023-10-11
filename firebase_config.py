import pyrebase

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