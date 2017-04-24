import psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs

def connectMessage():
    connection = 'dbname=chicken user=messagemanager password=XyshenSsintk343b5h3bn9ndjsuz9s76aISneksI host=localhost'
    print(connection)
    try:
        return psycopg2.connect(connection)
    except:
        print("Cannot connect to database")
    
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
    #print(query)
    #print(args)
    try:
        quer = cur.mogrify(query, args)
        #print(quer)
        cur.execute(quer)
        if select:
            results = cur.fetchall()
        conn.commit()
        #print(select)
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
    conn.close()
    cur.close()
    #print(results)
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
    
def addToUsers(fname, lname, username, password, email):
    #print("in addToUsers")
    conn = connectUsers()
    if conn == None:
        print("Cannot connect")
        return None
    qstring = "INSERT INTO users (firstname, lastname, username, password, email) VALUES (%s, %s, %s, crypt(%s, gen_salt('bf')), %s)"
    #print(qstring)
    executeQuery(qstring, conn, select=False, args=(fname, lname, username, password, email))
    conn.close()
    return 0
    
def checkexists(conn, track_id):
    cur = conn.cursor()
    try:
        qstring = cur.mogrify("SELECT username FROM users WHERE username = %s",(track_id,))
        cur.execute(qstring)
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
    chek = cur.fetchone() is not None
    conn.close()
    cur.close()
    return chek
    
def matchpassword(conn, trackpass, username):
    if conn == None:
        return None
    try:
        qstring = "SELECT username FROM users WHERE password=crypt(%s, password) AND username=%s"
        chek = executeQuery(qstring, conn, select=True, args=(trackpass, username))
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
        qstring = ""
    conn.close()
    print(chek)
    print(username)
    if chek[0][0] == username:
        return True
    else:
        return False
        
def sort(quer, arg):
    conn = connectMaster()
    curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print(quer)
    print(arg)
    if conn == None:
        return None
    try:
        qstring = curr.mogrify(quer % (arg[0]))
        print(qstring)
        curr.execute(qstring)
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
    if curr.rowcount > 0:
        return curr.fetchall()
    else:
        return None
    
def sortOwn(quer, arg1, arg2):
    conn = connectMaster()
    curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print("arguments:")
    print(quer)
    print(arg1)
    print(arg2)
    string = "'" + arg1 + "'"
    if conn == None:
        return None
    try:
        qstring = curr.mogrify(quer % (string, arg2[0]))
        print(qstring)
        curr.execute(qstring)
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
    if curr.rowcount > 0:
        return curr.fetchall()
    else:
        return None
        
def getUsers(conn):
    if conn == None:
        return None
    qstring = "SELECT username FROM users"
    chek = executeQuery(qstring, conn, True, args=None)
    return chek
    
def getAdmin(username, conn):
    if conn == None:
        return None
    cur = conn.cursor()
    qstring = "SELECT admin FROM users WHERE username=%s"
    chek = cur.mogrify(qstring, username)
    cur.execute(chek)
    return cur.fetchall()
    
def addToMessages(username, msg):
    conn = connectMaster()
    if conn == None:
        return None
    qstring = "SELECT userid FROM users WHERE username=%s"
    id = executeQuery(qstring, conn, True, args=[username])
    print(id)
    qstring = "INSERT INTO messages (userid, message) VALUES (%s, %s)"
    conn = connectMaster()
    if conn == None:
        print("Couldn't connect to database")
        return None
    executeQuery(qstring, conn, False, args=(id[0][0], msg))
    return 0
    
def getMessages():
    conn = connectMessage()
    if conn == None:
        print("Cannot connect")
        return None
    qstring = "SELECT message FROM messages"
    #print("Message: ", qstring)
    chek = executeQuery(qstring, conn)
    return chek
    
def getUserForMessage():
    conn = connectMaster()
    if conn == None:
        print("Cannot connect")
        return None
    qstring = "SELECT users.username FROM messages INNER JOIN users ON messages.userid = users.userid"
    #print("User: ", qstring)
    chek = executeQuery(qstring, conn)
    return chek