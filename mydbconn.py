import mysql.connector

def mydb():
    try:
        mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "admin", database = "crypto_storage")
        return mydb
    except Exception as e:
        # print(e)
        return e