import psycopg2
import psycopg2.extras

def connectSugg():
    connection = 'dbname=chicken user=sugmanager password=PuBuY5pRuw2YeHaBeN7pAcu2eH2nas4u host=localhost'
    print(connection)
    try:
        return psycopg2.connect(connection)
    except:
        print("Cannot connect to database")
        
def connectUsers():
    connection = 'dbname=chicken user=usermanager password=HeWudrasEnamEkEcHuqUzatrEdE3AbAp host=localhost'
    print(connection)
    try:
        return psycopg2.connect(connection)
    except:
        print("Cannot connect to database")
        
def connectMaster():
    connection = 'dbname=chicken user=mastermanager password=dR7ha66feguprutha7UjebuspeTeRaja host=localhost'
    print(connection)
    try:
        return psycopg2.connect(connection)
    except:
        print("Cannot connect to database")
        
def executeQuery(query, conn, select=True, args=None):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    results = None
    try:
        quer = cur.mogrify(query, args)
        
        cur.execute(quer)
        if select:
            results = cur.fetchall()
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
    return results
    
def addToSuggestions(userid, sugtype, sug):
    print("Suggestions")
    conn = connectSugg()
    if conn == None:
        return None
    qstring = "INSERT INTO suggestions (userid, suggestiontype, suggestion, votes) VALUES (%s, %s, %s, 0)"
    print(qstring)
    executeQuery(qstring, conn, select=False, args=(userid[0][0], sugtype, sug))
    conn.close()
    return 0
    
def addToUsers(fname, lname, username, age, password, email):
    conn = connectUsers()
    if conn == None:
        return None
    qstring = "INSERT INTO users (firstname, lastname, username, age, password, email) VALUES (%s, %s, %s, %s, %s, %s)"
    print(qstring)
    executeQuery(qstring, conn, select=False, args=(fname, lname, username, age, password, email))
    conn.close()
    return 0
    
def checkexists(conn, track_id):
    cur = conn.cursor()
    try:
        cur.execute("SELECT username FROM users WHERE username = %s", (track_id,))
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
    chek = cur.fetchone() is not None
    conn.close()
    return chek
    
def matchpassword(conn, trackpass, username):
    cur = conn.cursor()
    if conn == None:
        return None
    try:
        qstring = "SELECT password FROM users WHERE username='%s'" % (username)
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
        qstring = ""
    chek = executeQuery(qstring, conn)
    conn.close()
    if chek[0][0] == trackpass:
        return True
    else:
        return False