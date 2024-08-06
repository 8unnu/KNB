import sqlite3

async def sql_operation(operation):
    connection = sqlite3.connect("knb_sqlite.db")

    cursor = connection.cursor()
    cursor.execute(operation)
    cursor.close()

    connection.commit()
    connection.close()

async def get_all_usernames():
    connection = sqlite3.connect("knb_sqlite.db")

    cursor = connection.cursor()
    cursor.execute("""SELECT username FROM users""")
    result = cursor.fetchall()
    cursor.close()

    connection.close()
    return result

async def get_user_password(username):
    connection = sqlite3.connect("knb_sqlite.db")

    cursor = connection.cursor()
    cursor.execute(f"""SELECT password FROM users WHERE username='{username}';""")
    result = cursor.fetchall()
    cursor.close()

    connection.close()
    return result

async def get_user_token(username):
    connection = sqlite3.connect("knb_sqlite.db")

    cursor = connection.cursor()
    cursor.execute(f"""SELECT jwt_token FROM users WHERE username='{username}';""")