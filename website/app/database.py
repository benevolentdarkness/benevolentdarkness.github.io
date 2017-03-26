import psycopg2
import psycopg2.extras

def connectSugg():
    connection = 'dbname=chicken user=sugmanager password=PuBuY5pRuw2YeHaBeN7pAcu2eH2nas4u host=localhost'
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
    cur.close()
    return results
    
def addToSuggestions(fname, lname, age, sugtype, sug):
    conn = connectSugg()
    if conn == None:
        return None
    qstring = "INSERT INTO suggestions (firstname, lastname, age, suggestiontype, suggestion, votes) VALUES ('%s', '%s', %s, '%s', '%s', 0)" % (fname, lname, age, sugtype, sug)
    print(qstring)
    executeQuery(qstring, conn, select=False, args=(fname, lname, age, sugtype, sug))
    conn.close()
    return 0