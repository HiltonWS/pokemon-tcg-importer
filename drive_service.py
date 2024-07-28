from io import BytesIO
import json
import os

from google.oauth2 import service_account

from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from googleapiclient.discovery import build

from config import DB_PATH, FOLDER_DATABASE_ID


def __service__():
    SERVICE_ACCOUNT_INFO = json.loads(os.getenv("GOOGLE_SERVICE_ACCOUNT_CREDENTIALS"))  # noqa: E501
    CREDENTIALS = service_account.Credentials.from_service_account_info(
        SERVICE_ACCOUNT_INFO,
        scopes=['https://www.googleapis.com/auth/drive']
    )

    return build('drive', 'v3', credentials=CREDENTIALS)


__DRIVE__ = __service__()


def __find_file_in_google_drive__():
    if FOLDER_DATABASE_ID:
        query = f"name = '{os.path.basename(DB_PATH)}' and trashed = false and '{FOLDER_DATABASE_ID}' in parents"  # noqa: E501
    results = __DRIVE__.files().list(q=query, spaces='drive', fields='files(id, name)').execute()   # noqa: E501
    items = results.get('files', [])
    if items:
        item = items[0]['id']
    return item


__FILE_ID__ = __find_file_in_google_drive__()


def download_from_google_drive():
    request = __DRIVE__.files().get_media(fileId=__FILE_ID__)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    with open(DB_PATH, 'wb') as f:
        fh.seek(0)
        f.write(fh.read())
    print(f"File downloaded successfully: {DB_PATH}")


def upload_to_google_drive():
    if __FILE_ID__:
        media = MediaFileUpload(DB_PATH, resumable=True)
        updated_file = __DRIVE__.files().update(fileId=__FILE_ID__, media_body=media).execute()  # noqa: E501
        print(f"File replaced successfully: {updated_file['name']}")
    else:
        file_metadata = {'name': os.path.basename(DB_PATH)}
        if FOLDER_DATABASE_ID:
            file_metadata['parents'] = [FOLDER_DATABASE_ID]
        media = MediaFileUpload(DB_PATH, resumable=True)
        __DRIVE__.files().create(body=file_metadata, media_body=media, fields='id').execute()  # noqa: E501
        print("File uploaded successfully")
