import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'user',
  'password': 'password',
  'host': '127.0.0.1',
  'database': 'SocialNetwork'
}

def connectDB(user=None, password=None):
    if user is not None:
        config['user'] = user
    if password is not None:
        config['password'] = password
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        # print("Connected successfully")
        return cnx

def disconnectDB(cnx):
    cnx.close()