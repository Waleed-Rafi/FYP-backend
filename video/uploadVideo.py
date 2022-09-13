import pyrebase
import datetime

config = {
    "apiKey": "AIzaSyAbBXSdQSUs-uHgmY6p1Jiw3L_vhwUlkhA",
    "authDomain": "intelligent-vs.firebaseapp.com",
    "projectId": "intelligent-vs",
    "storageBucket": "intelligent-vs.appspot.com",
    "databaseURL": "",
    "messagingSenderId": "913340539374",
    "appId": "1:913340539374:web:49460dadf9decba5f0aeff",
    "measurementId": "G-9N6TEX71X0",
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
# Create Authentication user account in firebase
auth = firebase.auth()


def uploadNewVideoFunction(mysql, cur, userId, path_local):
    response = {"body": {"message": "Successfully created"}, "status": 201}
    try:
        ct = datetime.datetime.now()
        ts = ct.timestamp()

        path_on_cloud = f"""output/myVideo{ts}.mp4"""
        # path_local = "fb_data/outputs/result.mp4"

        storage.child(path_on_cloud).put(path_local)

        # Enter your user account details
        email = "waleed.rafi626@gmail.com"
        password = "waleed123"

        user = auth.sign_in_with_email_and_password(email, password)

        url = storage.child(path_on_cloud).get_url(user["idToken"])
        print(url)

        sql = "INSERT INTO VIDEO(videoUrl, userId) VALUES (%s, %s)"
        cur.execute(sql, (url, userId))
        mysql.connection.commit()

    except Exception as e:
        print(e)
        response = {"body": {"message": "Error Uploading Video"}, "status": 400}

    return response
