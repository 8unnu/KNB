import sqlite3

# ----------------------------------------------------------------------------------------------------------------------
# create table
# operation = f'''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255), password VARCHAR(16));'''
# operation = f'''CREATE TABLE IF NOT EXISTS game_data (win INTEGER, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id));'''
# ----------------------------------------------------------------------------------------------------------------------

# connection = sqlite3.connect("knb_sqlite.db")
#
# username = "bunnu2"
# cursor = connection.cursor()
# cursor.execute(f"""SELECT password FROM users WHERE username='{username}';""")
# result = cursor.fetchall()
# cursor.close()
#
# connection.close()
#
# print(result[0][0])

connection = sqlite3.connect("knb_sqlite.db")

cursor = connection.cursor()
cursor.execute(f'''CREATE TABLE IF NOT EXISTS game_data (win INTEGER, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id));''')
print('complete')
cursor.close()

connection.commit()
connection.close()

# def res_converter(a):
#     if a == 1:
#         return ["Win", "Lose"]
#     else:
#         return ["Lose", "Win"]
#
# user_id = 3
# connection = sqlite3.connect("knb_sqlite.db")
# cursor = connection.cursor()
# cursor.execute(f'''SELECT win FROM game_data WHERE user_id={user_id};''')
# result = cursor.fetchall()
# cursor.close()
#
# connection.close()
#
# print(result)
#
# for i in reversed(result):
#     res_arr = res_converter(i[0])
#     print(f"You {res_arr[0]}, AI {res_arr[1]}")