from __future__ import print_function
import auth
import fixture
import itemDeDrive
import emailSend
import emailSend
import driveProject
import database
import easygui
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from configparser import SafeConfigParser


if __name__ == '__main__':
    dbSettings = SafeConfigParser()
    dbSettings.read(easygui.fileopenbox(msg = "Indicar archivo de coneccion a la base", title = "Seleccionar archivo", filetypes = "*.ini"))
    # Scopes que dan acceso a la API
    DRIVE_SCOPE = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/gmail.readonly']
    CLIENT_SECRET_FILE = easygui.fileopenbox(msg = "Indicar JSON de API's", title = "Seleccionar archivo", filetypes = "*.json") # Debe estar ubicado en un lugar donde quien lo ejecute solamente tenga acceso.
    DRIVE_APPLICATION_NAME = 'Google Drive API'
    authInstance = auth.auth(DRIVE_SCOPE,CLIENT_SECRET_FILE,DRIVE_APPLICATION_NAME)
    credentials = authInstance.get_credentials()
    http = credentials.authorize(httplib2.Http())
    driveService = discovery.build('drive', 'v3', http=http)
    gmailService = discovery.build('gmail', 'v1', http=http)


    driveInstance = driveProject.driveClass(driveService)
    gmailInstance = emailSend.mailService(gmailService)
    databaseInstance = database.databaseInstance(dbSettings.get('config','lh'),dbSettings.get('config','un'),dbSettings.get('config','pw'),dbSettings.get('config','db'))
    databaseInstance.connect()
    databaseInstance.createIfNotExists() # Se crean las tablas en caso de que no existan

    items = driveInstance.getFiles(100)
    if not items:
        print('No files found.')
    else:
        for item in items:
            itemInstance = itemDeDrive.itemDeDrive( # Llamo desde fixture para que no sea engorroso.
                fixture.getItemId(item),
                fixture.getName(item),
                fixture.getFileExtension(item),
                fixture.getOwnerDisplayName(item),
                fixture.getOwnerEmailAddress(item),
                fixture.getFileAccess(item),
                fixture.getLastChangeDate(item))
            if(itemInstance.VISIBILIDAD == True): # Verifico si el item esta Publico "True" / Privado "False"
                itemInstance.deletePublicPermissions(driveService) # Le quito los permisos de "Publico"
                databaseInstance.insertNewPublicItem(itemInstance) # Inserto el item en la base de documentos que alguna vez fueron públicos
                message = gmailInstance.create_message(gmailInstance.getMyEmailAddress(gmailService),itemInstance.OWNER_MAIL,'Aviso de modificación de archivo','Te aviso que modifique la visibilidad de tu archivo: '+itemInstance.NOMBRE_ARCHIVO)
                gmailInstance.send_message("me",message) # Como está público envío el correo al owner
            if(databaseInstance.itemIsNotPresentInDB(itemInstance)):
                databaseInstance.insertNewItem(itemInstance) # Inserto el item en la base de datos
            else:
                databaseInstance.updateItem(itemInstance) # Actualizo el item de la base con el actual

    databaseInstance.close()
