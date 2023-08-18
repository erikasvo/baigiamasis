import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '1111'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE baigiamojodb")

print('run dbcon')