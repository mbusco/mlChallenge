from __future__ import print_function
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import os
import auth
import fixture
import itemDeDrive
import emailSend

class driveClass():

    def __init__(self,DRIVE_SERVICE):
        self.DRIVE_SERVICE = DRIVE_SERVICE

    def getFiles(self, size): # Solamente utiliza el servicio de drive para traerme los parametros que necesito
        results = self.DRIVE_SERVICE.files().list(pageSize=size,fields="nextPageToken, files(id, name, modifiedTime, owners, fileExtension, description, permissions)").execute()
        return results.get('files', [])
        