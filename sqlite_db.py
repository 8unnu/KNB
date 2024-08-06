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

async def get_user_id(username):
    connection = sqlite3.connect("knb_sqlite.db")

    cursor = connection.cursor()
    cursor.execute(f"""SELECT id FROM users WHERE username='{username}';""")
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

async def get_games_results_wins(user_id):
    connection = sqlite3.connect("knb_sqlite.db")

    cursor = connection.cursor()
    cursor.execute(f'''SELECT win FROM game_data WHERE user_id={user_id} AND win=1;''')
    result = cursor.fetchall()
    cursor.close()

    connection.close()
    return len(result)

async def get_games_results_loses(user_id):
    connection = sqlite3.connect("knb_sqlite.db")

    cursor = connection.cursor()
    cursor.execute(f'''SELECT win FROM game_data WHERE user_id={user_id} AND win=0;''')
    result = cursor.fetchall()
    cursor.close()

    connection.close()
    return len(result)