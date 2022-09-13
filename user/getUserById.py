def getUserByIdFunction(mysql, cur, userEmail):
    response = {
        "body": {
            "message": "Success"
        },
        "status": 200
    }
    try:
        sql = "Select * from USER where email = %s"
        cur.execute(sql, (userEmail))
        rv = cur.fetchall()
        response["body"]["data"] = rv
        mysql.connection.commit()
    except:
        response = {
            "body": {
                "message": "Something went wrong!"
            },
            "status": 400
        }

    return response
