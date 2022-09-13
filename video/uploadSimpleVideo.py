def uploadNewSimpleVideoFunction(mysql, cur, videoUrl, userId):
    response = {
        "body": {
            "message": "Successfully created"
        },
        "status": 201
    }
    try:
        sql = "INSERT INTO VIDEO(videoUrl, userId) VALUES (%s, %s)"
        cur.execute(sql, (videoUrl, userId))
        mysql.connection.commit()

    except Exception as e:
        print(e)
        response = {
            "body": {
                "message": "Error Uploading Video"
            },
            "status": 400
        }

    return response
