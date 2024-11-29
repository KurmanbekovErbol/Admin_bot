import sqlite3

connect = sqlite3.connect("Chat_users.db")
cursor = connect.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
telegram_id INTEGER,
name VARCHAR (64),
chat_id INT,
status_admin BOOLEAN NOT NULL DEFAULT FALSE
)
""")

def register(telegram_id, name, chat_id):
    cursor.execute(f"SELECT telegram_id FROM user WHERE telegram_id = ({telegram_id})")
    users = cursor.fetchall()
    if users:
        pass
    else:
        cursor.execute(f"INSERT INTO user (telegram_id, name, chat_id) VALUES ({telegram_id}, '{name}', {chat_id})")
        connect.commit()

def check_admins(telegram_id):
    cursor.execute(f"SELECT telegram_id FROM user WHERE telegram_id = ({telegram_id})")
    users = cursor.fetchall()
    if users:
        cursor.execute(f"SELECT status_admin FROM user WHERE telegram_id = ({telegram_id})")
        admin = cursor.fetchall()
        for i in admin:
            for a in i:
                if a == 1:
                    return a
                elif a == 0:
                    return a
                elif a == None:
                    return a           
    else:
        pass

def add_admins(telegram_id):
    cursor.execute(f"SELECT telegram_id FROM user WHERE telegram_id = ({telegram_id})")
    users = cursor.fetchall()
    if users:
        cursor.execute(f"UPDATE user SET status_admin = {True} WHERE telegram_id = {telegram_id}")
        connect.commit()
    else:
        pass

def demote_admin(telegram_id):
    cursor.execute(f"SELECT telegram_id FROM user WHERE telegram_id = ({telegram_id})")
    users = cursor.fetchall()
    if users:
        cursor.execute(f"UPDATE user SET status_admin = {False} WHERE telegram_id = {telegram_id}")
        connect.commit()
    else:
        pass
    
def get_chat_id():
    chat_id = cursor.execute("SELECT chat_id FROM user")
    chat_id = cursor.fetchall()
    list_chat_id = []
    for i in chat_id:
        list_chat_id.append(i[0])
    return list_chat_id

def get_users():
    users = cursor.execute("SELECT name FROM user")
    users = cursor.fetchall()
    list_users = []
    for i in users:
        list_users.append(i[0])
    return list_users

# add_admins() Введите телеграм id что бы стать админом