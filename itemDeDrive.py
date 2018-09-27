import emailSend
from apiclient import errors

class itemDeDrive():
    def __init__(self, ID, NOMBRE_ARCHIVO, EXTENSION, OWNER_NAME, OWNER_MAIL, VISIBILIDAD, FECHA_ULTIMA_MODIFICACION):
        self.ID = ID
        self.NOMBRE_ARCHIVO = NOMBRE_ARCHIVO
        self.EXTENSION = EXTENSION
        self.OWNER_NAME = OWNER_NAME
        self.OWNER_MAIL = OWNER_MAIL
        self.VISIBILIDAD = VISIBILIDAD
        self.FECHA_ULTIMA_MODIFICACION = FECHA_ULTIMA_MODIFICACION

    def deletePublicPermissions(self, drive_service): # Elimina los permisos de acceso publicos
        try:
            drive_service.permissions().delete(fileId= self.ID, permissionId= 'anyone').execute()
        except errors.HttpError as error:
            print('No se pudo quitar la autorización: {}'.format(error))
        try:
            drive_service.permissions().delete(fileId= self.ID, permissionId= 'anyoneWithLink').execute()
        except errors.HttpError as error:
            print('No se pudo quitar la autorización: {}'.format(error))