def createNewUserFunction(mysql, cur, username, email):
    response = {
        "body": {
            "message": "Successfully created"
        },
        "status": 201
    }
    try:
        sql = "INSERT INTO USER(username, email) VALUES (%s, %s)"
        cur.execute(sql, (username, email))
        mysql.connection.commit()
    except:
        response = {
            "body": {
                "message": "Error: User might already exist"
            },
            "status": 400
        }

    return response
