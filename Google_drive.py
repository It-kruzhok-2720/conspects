import pickle
from settings import  CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

class Google_drive:
    def __init__(self):
        self._root_folder = "Conspects"
        self.service = None
        self.mime_types = {"folder" : "application/vnd.google-apps.folder", "photo" : "application/vnd.google-apps.photo"}
        cred = None

        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
        # print(pickle_file)

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        self.service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')


    def create_new_folder(self, name, parent=""):
        parent_id = None
        if parent != "":
            parent_id = self._get_file_id(parent, "folder")[0]["id"]
        file_metadata = {
            "name" : name,
            "mimeType": self.mime_types[type],
            "parents" : [parent_id]
        }
        self.service.files().create(body=file_metadata).execute()

    """ def upload_photos(self, photos, folder):
        folder_id = self._get_file_id(folder)
        for index, photo in enumerate(photos):
            file_metadata = {
                'name': f'{index+1}.jpeg',

            }
    """

    def _get_file_id(self, name, type_of_file):
        mime_type = self.mime_types[type_of_file]
        files = self.service.files().list(corpora="user", includeItemsFromAllDrives=False, q=f"name = '{name}' and mimeType = '{mime_type}'").execute()["files"] 
        print(files)
        return files

    def empty_trash(self):
        self.service.files().emptyTrash().execute()