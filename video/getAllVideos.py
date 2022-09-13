def getAllVideosFunction(mysql, cur):
    response = {"body": {"message": "Success"}, "status": 200}
    try:
        sql = "Select * from VIDEO order by createDate desc"
        cur.execute(sql)
        rv = cur.fetchall()
        response["body"]["data"] = rv
        mysql.connection.commit()
    except:
        response = {"body": {"message": "Something went wrong!"}, "status": 400}

    return response
