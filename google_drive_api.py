from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = 'google_drive_api_key.json'
API_NAME = 'drive'
API_VESION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VESION, SCOPES)


def create_folder(folder_name, parent_id):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }
    folder = service.files().create(body=file_metadata).execute()
    return folder['id']


def upload_media_to_driver(folder_path, media_list, paren_id):
    media_file_list = []
    mime_type_list = []
    for video in media_list:
        media_file_list.append(video + '.mp3')
        media_file_list.append(video + '.mp4')
        mime_type_list.append('audio/mpeg')
        mime_type_list.append('video/mp4')
    for file, mime_type in zip(media_file_list, mime_type_list):
        file_metadata = {
            'name': file,
            'parents': [paren_id]
        }
        media = MediaFileUpload(folder_path + file, mimetype=mime_type)
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
