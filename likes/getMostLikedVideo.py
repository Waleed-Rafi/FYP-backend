def getMostLikedVideoFunction(mysql, cur):
    response = {"body": {"message": "Successfully Fetched!"}, "status": 201}
    try:
        sql = "SELECT * from (select videoId, userId, count(*) as totalLikes from LIKES group by videoId) as ABC"
        cur.execute(sql)
        rv = cur.fetchall()
        mysql.connection.commit()
        videoId = largest(rv, len(rv))
        print(videoId)
        sql = f"""SELECT * from VIDEO where id={videoId}"""
        cur.execute(sql)
        rv = cur.fetchall()
        mysql.connection.commit()
        response["body"]["videoData"] = rv[0]
    except:
        response = {"body": {"message": "Error: Something went wrong"}, "status": 400}

    return response


def largest(arr, n):

    # Initialize maximum element
    max = arr[0][2]
    videoId = arr[0][0]

    # Traverse array elements from second
    # and compare every element with
    # current max
    for i in range(1, n):
        if arr[i][2] > max:
            max = arr[i][2]
            videoId = arr[i][0]
    return videoId
