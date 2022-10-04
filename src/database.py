import sqlite3

DBPATH = "data/data.db"
USERS_TABLE = "users_table"
# holds {ownerID, canvasKey}
CLASSES_TABLE = "classes_table"
# holds {ownerID, className}
# examples
# {john, Math 420}
# {john, English 330}
# {smith, English 330}

def CreateDatabase():
    print(f"setting up database")
    con = sqlite3.connect(DBPATH)
    with con:
        cursor = con.cursor()
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {USERS_TABLE}(
        userID int UNIQUE, 
        canvasKey string)
        """)
        # FIXME todo
        cursor.execute(f""" 
        CREATE TABLE IF NOT EXISTS {CLASSES_TABLE}(
        userID int UNIQUE, 
        className string)
        """)
    con.close()
    print("finished")
    return

def VetUserID(userID): #FIXME Verify with discord 
    return len(str(userID)) == 18
        
def SearchUser(userID): # returns 0 if ownerID is not in DB
    con = sqlite3.connect(DBPATH)
    with con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT * FROM {USERS_TABLE} WHERE userID={userID}
        """)
    return len(cur.fetchall())

def FetchApiKey(ownerID):
    if searchOwner(ownerID):
        return
    con = sqlite3.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT * FROM {TABLE} WHERE user_id={ownerID}
        """)
        return cur.fetchone()

def AddUser(userID, canvasKey):
    if searchUser(userID):
        return
    con = sqlite3.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute(f"""
        INSERT INTO {USERS_TABLE} (userID, canvasKey)
        VALUES ('{userID}', '{canvasKey}')
        """)
    con.close()
    return

