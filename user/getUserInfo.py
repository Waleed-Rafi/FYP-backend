def getUserInfoFunction(mysql, cur, email):
    response = {
        "body": {
            "message": "Success"
        },
        "status": 200
    }
    try:
        sql = f'''Select * from USER where email={email}'''
        cur.execute(sql)
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
