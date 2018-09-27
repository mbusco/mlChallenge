import base64
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import mimetypes
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors

class mailService:

    def __init__(self,GMAIL_SERVICE):
        self.GMAIL_SERVICE = GMAIL_SERVICE

    def create_message(self, sender, to, subject, message_text): # metodo de armado del correo electronico
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        return {'raw': raw}   
   

    def send_message(self, user_id, message): # Metodo de envío
        message = (self.GMAIL_SERVICE.users().messages().send(userId=user_id, body=message).execute())
        return message

    def getMyEmailAddress(self,gmail_service): # Consultado para saber la dirección de correo electrónico del remitente
        return (gmail_service.users().getProfile(userId='me').execute()).get('emailAddress')