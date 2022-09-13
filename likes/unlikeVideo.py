def unlikeVideoFunction(mysql, cur, videoId, userId):
    response = {"body": {"message": "Successfully Deleted!"}, "status": 201}
    try:
        sql = f'''DELETE FROM LIKES WHERE videoId={videoId} and userId={userId}'''
        cur.execute(sql)
        mysql.connection.commit()
    except:
        response = {"body": {"message": "Error: Something went wrong"}, "status": 400}

    return response
