#!/usr/bin/python
import os,sqlite3
confighome = os.path.expanduser("~")+"/.config/pimagizer/conf.db"
if not os.path.exists(confighome):
    os.mkdir(os.path.expanduser("~")+"/.config/pimagizer/")
def createbase():
    print("Crear base")
    filebase = open(confighome,'w')
    filebase.close()
    conn = sqlite3.connect(confighome)
    c = conn.cursor()
    c.execute("CREATE TABLE config (id integer UNIQUE PRIMARY KEY, indice VARCHAR(30), value INTEGER)")
    c.execute("INSERT INTO config VALUES(NULL, 'width', 300)")
    c.execute("INSERT INTO config VALUES(NULL, 'height', 300)")
    c.execute("INSERT INTO config VALUES(NULL, 'newname', 1)")
    c.execute("INSERT INTO config VALUES(NULL, 'defaultpx', 1)")
    for row in c:
        print (row)
    conn.commit()
    c.close() 
def get_value(indice):
    conn = sqlite3.connect(confighome)
    c = conn.cursor()
    c.execute("SELECT value FROM 'config' WHERE indice='%s'" % indice)
    for row in c:
        value = row[0]
        #print value
    conn.commit()
    c.close()
    return int(value)
def set_value(indice,value):
    conn = sqlite3.connect(confighome)
    c = conn.cursor()
    valor = str(value)
    c.execute("UPDATE config SET value='"+valor+"' WHERE indice='%s'" %indice)
    #print "valor",value,"from",indice
    conn.commit()
    c.close()
def new_value(indice,value):
    conn = sqlite3.connect(confighome)
    c = conn.cursor()
    valor = str(value)
    c.execute("INSERT INTO config VALUES(NULL, '" + indice + "', " + str(value) + ")")
    conn.commit()
    c.close()
def try_value(indice,value): #tries if exist indice on database. If exists: nothing, else creates a indice with indicated value
    try:
        get_value(indice)
    except:
        new_value(indice,value)
        print("value of",indice,":",get_value(indice))
    finally:
        print("value",indice,"exists: ",get_value(indice))

