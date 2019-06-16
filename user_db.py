import sqlite3

con = sqlite3.connect('tipsugar.db')
cur = con.cursor()
create_table = '''CREATE TABLE IF NOT EXISTS userlist(user_id TEXT, name TEXT)'''
cur.execute(create_table)

def add_user(user_id, name):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()

    sql = 'INSERT INTO userlist (user_id, name) VALUES (?,?)'
    user = (user_id, name)
    cur.execute(sql, user)
    con.commit()
    con.close()

def check_user(id):
    con = sqlite3.connect('tipsugar.db')
    cur = con.cursor()

    cur.execute('SELECT * FROM userlist WHERE user_id={0}'.format(id))
    if cur.fetchall() == []:
        return False
    else:
        return True