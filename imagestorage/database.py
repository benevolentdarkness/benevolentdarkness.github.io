import psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs

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
    
def addToImages(link, username):
    conn = None
    query = "SELECT userid FROM users WHERE username=%s"
    args = (username)
    x = executeQuery(query, conn, True, args)
    qstring = "INSERT INTO images (userid, link) VALUES (%s, %s)"
    args2 = (x[0][0], link)
    executeQuery(qstring, conn, False, args2)
    return None
    
def addToUsers(username, password):
    conn = None
    qstring = "INSERT INTO users (username, password) VALUES (%s, crypt(%s, gen_salt('bf')))"
    args = (username, password)
    executeQuery(qstring, conn, False, args)
    return None