import psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs

def connectMaster():
    connection = "dbname=imagestorage user=mastermanager password=dR7ha66feguprutha7UjebuspeTeRaja host=localhost"
    try:
        return psycopg2.connect(connection)
    except:
        print("Cannot connect")

def executeQuery(query, conn, select=True, args=None):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    results = None
    (query)
    (args)
    try:
        quer = cur.mogrify(query, args)
        (quer)
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
    
def addToImages(link, imagename, username, private):
    print("Got to images")
    conn = connectMaster()
    query = "SELECT userid FROM users WHERE username=%s"
    args = [username]
    print(username)
    x = executeQuery(query, conn, True, args)
    conn = connectMaster()
    qstring = "INSERT INTO images (imagename, link, privacy) VALUES (%s, %s, %s)"
    args2 = (imagename, link, private)
    executeQuery(qstring, conn, False, args2)
    conn = connectMaster()
    query2 = "SELECT imageid FROM images WHERE link=%s"
    args3 = [link]
    print(link)
    y = executeQuery(query2, conn, True, args3)
    conn = connectMaster()
    qstring2 = "INSERT INTO userimage (userid, imageid) VALUES (%s, %s)"
    args4 = (x[0][0], y[0][0])
    print(x)
    print(y)
    executeQuery(qstring2, conn, False, args4)
    return None
    
def addToUsers(username, password):
    conn = connectMaster()
    qstring = "INSERT INTO users (username, password) VALUES (%s, crypt(%s, gen_salt('bf')))"
    args = (username, password)
    executeQuery(qstring, conn, False, args)
    return None
    
#Adds a tag to an image
def addToTags(link, tag):
    print("Got to tags")
    conn = connectMaster()
    find = "SELECT tagid FROM tags WHERE name=%s"
    linker = "SELECT DISTINCT imageid FROM images WHERE link=%s"
    args = [tag]
    linkargs = [link]
    print(linkargs)
    x = executeQuery(find, conn, True, args)
    print(x)
    conn = connectMaster()
    y = executeQuery(linker, conn, True, linkargs)
    print(y)
    conn = connectMaster()
    if x:
        connect = "INSERT INTO tagmanager (imageid, tagid) VALUES (%s, %s)"
        args2 = (y[0][0], x[0][0])
        executeQuery(connect, conn, False, args2)
    else:
        query1 = "INSERT INTO tags (name) VALUES (%s)"
        args1 = [tag]
        executeQuery(query1, conn, False, args1)
        conn = connectMaster()
        find = "SELECT tagid FROM tags WHERE name=%s"
        args = [tag]
        x = executeQuery(find, conn, True, args)
        conn = connectMaster()
        connect = "INSERT INTO tagmanager (imageid, tagid) VALUES (%s, %s)"
        print(y)
        print(x)
        args2 = (y[0][0], x[0][0])
        executeQuery(connect, conn, False, args2)
    return None

#Returns all tags associated with an image
def getTagsFromLink(link):
    conn = connectMaster()
    qstring = "SELECT tags.name FROM tags INNER JOIN tagmanager ON tags.tagid = tagmanager.tagid INNER JOIN images ON tagmanager.imageid = images.imageid WHERE images.link=%s"
    args = (link)
    return executeQuery(qstring, conn, True, args)
    
#Returns all tags
def getTags():
    conn = connectMaster()
    qstring = "SELECT DISTINCT name FROM tags"
    return executeQuery(qstring, conn)
    
def getUserFromLink(link):
    conn = connectMaster()
    qstring = "SELECT users.username FROM users INNER JOIN userimage ON users.userid = userimage.userid INNER JOIN images ON userimage.imageid = images.imageid WHERE images.link=%s"
    args = (link)
    return executeQuery(qstring, conn, True, args)
    
def getUsers():
    conn = connectMaster()
    qstring = "SELECT DISTINCT username FROM users"
    return executeQuery(qstring, conn)
    
def login(username, password):
    conn = connectMaster()
    qstring = "SELECT username FROM users WHERE username=%s AND password=crypt(%s, password)"
    args = (username, password)
    x = executeQuery(qstring, conn, True, args)
    print(username)
    print(x)
    if x[0][0] == username:
        return True
    else:
        return False
    
def checkExists(username):
    conn = connectMaster()
    cur = conn.cursor()
    print(username)
    try:
        qstring = cur.mogrify("SELECT username FROM users WHERE username = %s", [username])
        cur.execute(qstring)
    except Exception as e:
        conn.rollback()
        print(type(e))
        print(e)
    if cur.fetchone() != None:
        check = True
    else:
        check = False
    conn.close()
    cur.close()
    return check
    
def getPublicImages():
    conn = connectMaster()
    qstring = "SELECT imagename, link FROM images WHERE privacy=%s"
    args = ("1")
    return executeQuery(qstring, conn, True, args)
    
def splitText(text):
    words = text.split()
    return words
    
def search(text):
    conn = connectMaster()
    qstring= "SELECT images.imagename, images.link FROM images INNER JOIN tagmanager ON images.imageid = tagmanager.imageid INNER JOIN tags ON tagmanager.tagid = tags.tagid WHERE tags.name=%s AND images.privacy=1"
    args = [text]
    return executeQuery(qstring, conn, True, args)