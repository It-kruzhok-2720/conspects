from distutils import extension
import pickle
from settings import  CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

class Conspects_storage:
    def __init__(self):
        #Создаем сервис, который общается с google api
        self.service = None 

        #Это херня, которая нужна для гугл диска, чтобы определять типы файлов
        self.mime_types = {"folder" : "application/vnd.google-apps.folder", "photo" : "application/vnd.google-apps.photo"}
        cred = None

        #Эта хуйня создаёт зашифрованный файл, в котором хранится токен
        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
        # print(pickle_file)

        #Если у нас есть файл с токеном, то мы его открываем
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        #Как я понял, если у нас нет токена, мы создаём его
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

    def upload_conspect(self, user, subject, date, files_path):
        #Папка юзера:
        #           Папка предмета:
        #                          Папка конспекта
        
        #Ищем id папки предмета
        user_folder_id = self.get_file_id(user, "folder")[0]["id"]
        subject_folder_id = self.get_file_id(subject, "folder", user_folder_id)[0]["id"]

        #Создаём новую папку конспекта и сохраняем её id
        new_conspect_folder_id = self.create_new_folder(date, subject_folder_id)["id"]
        
        #Загружаем только фотографии
        files = os.listdir(files_path)
        for file in files:
            self.upload_photo(file, files_path, new_conspect_folder_id)

    def create_new_folder(self, name, parent_id=""):
        folder_metadata = {
            "name" : name,
            "mimeType": self.mime_types["folder"],
        }
        
        #Если новая папка будет находится внутри другой, мы должны указать id другой папки
        if parent_id != "":
            folder_metadata["parents"] = [parent_id]
        
        #Возвращаем ответ Google Drive API
        return self.service.files().create(body=folder_metadata, fields='id').execute()

    def upload_photo(self, photo, folder_path, folder_id):
        name = photo.split('.')[0]
        extension = photo.split('.')[-1]
        full_path = folder_path + '/' + photo

        file_metadata = {
            'name': name,
            'parents' : [folder_id]
        }

        media = MediaFileUpload(full_path, f'image/{extension}')

        #Возвращаем ответ Google Drive API
        return self.service.files().create(body=file_metadata, media_body=media).execute()

    def get_file_id(self, name, type_of_file, parent=""):
        mime_type = self.mime_types[type_of_file]
        
        #Если искомый файл находится внутри папки, мы должны указать id папки
        if parent != "": 
            parent = f"and '{parent}' in parents"
        
        files = self.service.files().list(corpora="user", includeItemsFromAllDrives=False, q=f"name = '{name}' and mimeType = '{mime_type}' and trashed = false {parent}").execute()["files"] 
        
        #Возвращаем ответ Google Drive API
        return files

    def empty_trash(self):
        #Возвращаем ответ Google Drive API
        return self.service.files().emptyTrash().execute()