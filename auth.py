from apiclient import discovery
from oauth2client import client, tools, file
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.discovery import build
from httplib2 import Http
import httplib2
import os

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

class auth:
    
    def __init__(self, SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME):
        self.SCOPES = SCOPES
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.APPLICATION_NAME = APPLICATION_NAME
    
    def get_credentials(self):
        try:
            cwd_dir = os.getcwd()
            credential_dir = os.path.join(cwd_dir, '.credentials')
            if not os.path.exists(credential_dir):
                os.makedirs(credential_dir)
            credential_path = os.path.join(credential_dir, 'credentials.json')
            store = file.Storage(credential_path) 
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            credentials = tools.run_flow(flow, store, flags)
            os.remove(credential_path) # Elimino store y archivo de credenciales
            os.rmdir(credential_dir)
            return credentials
        except ValueError:
            print('Hubo un error de credenciales')