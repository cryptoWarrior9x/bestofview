from Google import Create_Service
from googleapiclient.http import MediaFileUpload

CLIENT_SECRET_FILE = 'google_drive_api_key.json'
API_NAME = 'drive'
API_VESION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VESION, SCOPES)

folders = ['test1', 'test 2']

for folder in folders:
    file_metadata = {
        'name': folder,
        'mimeType': 'application/vnd.google-apps.folder'
        # 'parents': []
    }
    x = service.files().create(body=file_metadata).execute()
    print('xxxx')  # x['id']
'''
folder_id = '1CMhystOuuH811QLqNI3Xf1T-Nj6f8oy5'
file_names = ['audio.mp3', 'download.mp4']
mime_types = ['audio/mpeg', 'video/mp4']
for file, mime_type in zip(file_names, mime_types):
    file_metadata = {
        'name': file,
        'parents': [folder_id]
    }
    media = MediaFileUpload(file, mimetype=mime_type)
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
'''