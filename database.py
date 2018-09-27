import mysql.connector
from mysql.connector.errors import Error

class databaseInstance():

    def __init__(self, HOSTSOURCE, USER_NAME, PASSWORD, DATABASE_SCHEMA):
        self.HOSTSOURCE = HOSTSOURCE
        self.USER_NAME = USER_NAME
        self.PASSWORD = PASSWORD
        self.DATABASE_SCHEMA = DATABASE_SCHEMA
    
    def connect(self):
       try:
            self.CONNECTOR = mysql.connector.connect(
            host= self.HOSTSOURCE,
            user= self.USER_NAME,
            passwd= self.PASSWORD,
            database= self.DATABASE_SCHEMA
            )
       except mysql.connector.Error as error:
            print('Hubo un error en la conexión: {}'.formar(error))
    
    def close(self):
        try:
            self.CONNECTOR.close()
        except mysql.connector.Error as error:
            print('Hubo un error cerrando la conexión: {}'.format(error))

    def createIfNotExists(self):
        try:
            sql = "show tables where Tables_in_driveappschema = 'itemstable'"
            mycursor = self.CONNECTOR.cursor()
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            if (len(myresult) == 0):
                mycursor.execute('CREATE TABLE itemstable (   FILE_ID varchar(100) NOT NULL,   NAME varchar(200) DEFAULT NULL,   EXTENSION varchar(45) DEFAULT NULL,   OWNER_NAME varchar(45) DEFAULT NULL,   OWNER_EMAIL varchar(45) DEFAULT NULL,   VISIBILITY varchar(45) DEFAULT NULL,   LAST_MODIFICATION_DATE varchar(45) DEFAULT NULL,   PRIMARY KEY (FILE_ID))')
            sql = "show tables where Tables_in_driveappschema = 'publicitemshistory'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            if (len(myresult) == 0):
                mycursor.execute('CREATE TABLE publicitemshistory ( FILE_ID varchar(100) NOT NULL, PRIMARY KEY (FILE_ID))')
            mycursor.close()
        except mysql.connector.Error as error:
            print('Hubo un error al crear las bases: {}'.format(error))

    def insertNewItem(self,item):
        try:
            sql = 'INSERT INTO itemstable (FILE_ID, NAME, EXTENSION, OWNER_NAME, OWNER_EMAIL, VISIBILITY, LAST_MODIFICATION_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            val = (item.ID, item.NOMBRE_ARCHIVO, item.EXTENSION, item.OWNER_NAME, item.OWNER_MAIL, item.VISIBILIDAD, item.FECHA_ULTIMA_MODIFICACION)
            mycursor = self.CONNECTOR.cursor()
            mycursor.execute(sql, val)
            self.CONNECTOR.commit()
            mycursor.close()
        except mysql.connector.Error as error:
            print('El item ya esta cargado en la base: {}'.format(error))

    def insertNewPublicItem(self,item):
        try: 
            sql = 'INSERT INTO publicitemshistory (FILE_ID) VALUES (%s)'
            val = (item.ID,)
            mycursor = self.CONNECTOR.cursor()
            mycursor.execute(sql, val)
            self.CONNECTOR.commit()
            mycursor.close()
        except mysql.connector.Error as error:
            print('El item ya esta cargado en la base: {}'.format(error))

    def itemIsNotPresentInDB(self,item):
        try:
            sql = 'SELECT FILE_ID FROM itemstable WHERE FILE_ID = %s'
            fileId = (item.ID, )
            mycursor = self.CONNECTOR.cursor()
            mycursor.execute(sql, fileId)
            myresult = mycursor.fetchall()
            mycursor.close()
            return len(myresult) == 0;
        except mysql.connector.Error as error:
            print('Hubo un inconveniente al realizar la busqueda: {}'.format(error))
            return True
    
    def updateItem(self, item):
        pass
