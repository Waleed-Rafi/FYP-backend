def addNewLikeToVideoFunction(mysql, cur, videoId, userId):
    response = {
        "body": {
            "message": "Successfully created"
        },
        "status": 201
    }
    try:
        sql = "INSERT INTO LIKES(videoId, userId) VALUES (%s, %s)"
        cur.execute(sql, (videoId, userId))
        mysql.connection.commit()
    except:
        response = {
            "body": {
                "message": "Error: Something went wrong"
            },
            "status": 400
        }

    return response
