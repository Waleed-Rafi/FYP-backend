from unittest import result
from flask import Flask, request
import os
import urllib
import requests
import face_blur
import face_reenactment
import time
import moviepy.editor
from moviepy.editor import *
import shutil


from flask_mysqldb import MySQL
from likes.addNewLikeToVideo import addNewLikeToVideoFunction
from user.createNewUser import createNewUserFunction
from user.getAllUsers import getAllUsersFunction
from user.getUserById import getUserByIdFunction
from video.getAllVideos import getAllVideosFunction
from video.uploadSimpleVideo import uploadNewSimpleVideoFunction
from video.uploadVideo import uploadNewVideoFunction
from likes.getMostLikedVideo import getMostLikedVideoFunction
from likes.unlikeVideo import unlikeVideoFunction
from flask_cors import CORS, cross_origin


app = Flask(__name__)

CORS(app)

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "video_streamer"

mysql = MySQL(app)


def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen(
        "ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(
            input=avi_file_path, output=output_name
        )
    )
    return True


@app.route("/face_blur", methods=["POST", "GET"])
def face_blur_api():
    if request.method == "POST":
        ADD_AUDIO = True
        body = request.json
        input_video_url = body["video_url"]
        ref_face_img_url = body["image_url"]
        output_path = "fb_data/outputs/result.avi"

        input_video_path = "fb_data/inputs/input_video.mp4"
        ref_face_img_path = "fb_data/inputs/ref_face_img.jpg"

        # Downloading Input Video
        urllib.request.urlretrieve(input_video_url, input_video_path)
        print("Input video for face_blur downloaded!")

        # Downloading Reference Image
        img_data = requests.get(ref_face_img_url).content
        with open(ref_face_img_path, "wb") as handler:
            handler.write(img_data)
        print("Input reference image for face_blur downloaded!")

        if ADD_AUDIO:
            # Extracting audio from the source video
            video = moviepy.editor.VideoFileClip(input_video_path)
            audio = video.audio
            audio.write_audiofile("fb_data/outputs/source_audio.mp3")

        # Applying Blur (max 1500 frames (last ~1597))
        face_blur.apply_blur(input_video_path, ref_face_img_path, output_path)
        # face_blur.apply_blur()
        print("Face Blur Applied!")
        result_path = output_path[:-3] + "mp4"

        if ADD_AUDIO:
            # Adding audio to result(video file)
            videoclip = VideoFileClip(output_path)
            audioclip = AudioFileClip("fb_data/outputs/source_audio.mp3")
            new_audioclip = CompositeAudioClip([audioclip])
            videoclip.audio = new_audioclip
            videoclip.write_videofile(result_path)
        else:
            # Video Conversion
            convert_avi_to_mp4(avi_file_path=output_path, output_name=output_path[:-4])
            time.sleep(60)
            print("Video Converted")

        print("FaceBlur results saved at: ", result_path)

        # Uploading results...
        print("Uploading results...")
        cur = mysql.connection.cursor()
        res = uploadNewVideoFunction(mysql, cur, 1, result_path)
        print(res)

        # Deleting results
        file_path = result_path
        if os.path.isfile(file_path):
            os.remove(file_path)
            print("File has been deleted")
        else:
            print("File does not exist")

        return {"status": "Success"}
    else:
        return {"status": "Success"}


@app.route("/face_reenactment", methods=["POST", "GET"])
def face_reenactment_api():
    if request.method == "POST":
        # Get URLS
        body = request.json

        input_image_url = body["input_image_url"]
        input_pose_src_url = body["input_pose_src_url"]
        input_audio_src_url = body["input_audio_src_url"]

        # Assigning Paths
        output_path = "misc/demo.csv"
        input_image_path = "misc/Input/0001/0001.jpg"
        input_pose_src_path = "misc/Pose_Source/1234.mp4"
        input_audio_src_path = "misc/Audio_Source/001.mp4"

        # Downloading Input Video's
        urllib.request.urlretrieve(input_pose_src_url, input_pose_src_path)
        urllib.request.urlretrieve(input_audio_src_url, input_audio_src_path)

        # Downloading Input Image
        img_data = requests.get(input_image_url).content
        with open(input_image_path, "wb") as handler:
            handler.write(img_data)

        # Applying Face reenactment
        face_reenactment.apply_reenactment(
            input_image_path, input_pose_src_path, input_audio_src_path, output_path
        )

        time.sleep(1000)
        print("Delay completed.")

        # Uploading to Firebase
        result_path = "results/id_0001_pose_1234_audio_001/avG_Pose_Driven_.mp4"
        cur = mysql.connection.cursor()
        res = uploadNewVideoFunction(mysql, cur, 1, result_path)
        print(res)

        # Deleting folder
        # shutil.rmtree(
        #     "results/id_0001_pose_1234_audio_001", ignore_errors=False, onerror=None
        # )

        return {"status": "Success"}
    else:
        return {"status": "Not Post request"}


@app.route("/")
def testApi():
    return {"success": "200", "message": "test api"}


@app.route("/create/user", methods=["POST"])
def createUser():
    cur = mysql.connection.cursor()
    request_data = request.get_json()

    username = request_data["username"]
    email = request_data["email"]

    res = createNewUserFunction(mysql, cur, username, email)

    return res["body"], res["status"]


@app.route("/user/info")
def userInfo():
    cur = mysql.connection.cursor()
    email = request.args.get('email')
    print(email)

    res = getAllUsersFunction(mysql, cur)

    return res["body"], res["status"]


@app.route("/users/all", methods=["GET"])
def getAllUsers():
    cur = mysql.connection.cursor()

    res = getAllUsersFunction(mysql, cur)

    return res["body"], res["status"]


@app.route("/user/find", methods=["POST"])
def getUserById():
    request_data = request.get_json()

    userEmail = request_data["email"]
    print(userEmail)
    cur = mysql.connection.cursor()

    res = getUserByIdFunction(mysql, cur, userEmail)

    return res["body"], res["status"]


# --------------- VIDEO --------------------
@app.route("/videos/all", methods=["GET"])
def getAllVideos():
    cur = mysql.connection.cursor()

    res = getAllVideosFunction(mysql, cur)

    return res["body"], res["status"]


# FOR TESTING
@app.route("/upload/video", methods=["POST"])
def uploadVideo():
    cur = mysql.connection.cursor()
    request_data = request.get_json()

    userId = request_data["userId"]

    res = uploadNewVideoFunction(mysql, cur, userId)

    return res["body"], res["status"]


@app.route("/upload/video/simple", methods=["POST"])
def uploadSimpleVideo():
    cur = mysql.connection.cursor()
    request_data = request.get_json()

    videoUrl = request_data["videoUrl"]
    userId = request_data["userId"]

    res = uploadNewSimpleVideoFunction(mysql, cur, videoUrl, userId)

    return res["body"], res["status"]


# --------------- LIKES --------------------
@app.route("/video/like", methods=["POST"])
def addLikeToVideo():
    cur = mysql.connection.cursor()
    request_data = request.get_json()

    videoUrl = request_data["videoId"]
    userId = request_data["userId"]

    res = addNewLikeToVideoFunction(mysql, cur, videoUrl, userId)

    return res["body"], res["status"]

# -------------- current user likes -------------------
@app.route("/video/like/user", methods=["POST"])
def addLikeToVideo():
    cur = mysql.connection.cursor()
    request_data = request.get_json()

    userId = request_data["userId"]

    res = addNewLikeToVideoFunction(mysql, cur, videoUrl, userId)

    return res["body"], res["status"]


# --------------- LIKES --------------------
@app.route("/video/unlike", methods=["POST"])
def unLikeVideo():
    cur = mysql.connection.cursor()
    request_data = request.get_json()

    videoId = request_data["videoId"]
    userId = request_data["userId"]

    res = unlikeVideoFunction(mysql, cur, videoId, userId)

    return res["body"], res["status"]


# --------------- GET MOST LIKED VIDEO --------------------
@app.route("/video/liked")
def mostLiked():
    cur = mysql.connection.cursor()

    res = getMostLikedVideoFunction(mysql, cur)

    return res["body"], res["status"]


if __name__ == "__main__":
    app.run(debug=True)
