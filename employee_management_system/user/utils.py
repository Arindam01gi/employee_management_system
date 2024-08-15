import hashlib
import os
import google.auth
import mimetypes
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

def getMd5Hash(string):
    md5_hash = hashlib.md5(string.encode()).hexdigest()
    return md5_hash

# def upload_to_google_drive(file_path,file_name):
#     SCOPES = ['https://www.googleapis.com/auth/drive.file']
#     SERVICE_ACCOUNT_FLE = 'E:\Employee_managemnt_system\employee_management_system\Google_drive_client_secret.json'
    
#     credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FLE,scopes=SCOPES)
    
#     service = build('drive','v3',credentials=credentials)
#     file_metadata = {'name':file_name}
#     media = MediaFileUpload(file_path,resumable=True)
#     file = service.files().create(body=file_metadata,media_body=media,fields='id').execute()
    
#     return file.get('id')
def get_mime_types(file_name):
    mime_type,_ = mimetypes.guess_type(file_name)
    return mime_type

def upload_to_google_drive(file_path,file_name,mime_type=None):
    
    if mime_type is None:
        mime_type = get_mime_types(file_name)
        
    creds, _ = google.auth.default()
    
    try:
        service = build("drive", "v3", credentials=creds)
        
        file_metadata = {
            "name": file_name,
            "mimeType": mime_type
        }
        media = MediaFileUpload(file_path,resumable=True)
        file = service.files().create(
            body = file_metadata,
            media_body = media,
            fields="id"
        ).execute()
        
        print(f'File with ID: "{file.get("id")}" has been uploaded.')
        return file.get("id")
    
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
        