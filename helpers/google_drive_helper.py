from apiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http
from helpers.io_helper import create_folder_if_not_exist
from apiclient.http import MediaIoBaseDownload
import io


def _filter_non_photos(item):
    non_photo_asset_names = [
        '.DS_Store',
        '100MSDCF'
    ]
    return item['name'] not in non_photo_asset_names


class GoogleDriveHelper:

    pageSize = 100

    def __init__(self, local_root_dir):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('credentials.json')
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store)

        self.service = build('drive', 'v3', http=creds.authorize(Http()))
        self.local_root_dir = local_root_dir
        create_folder_if_not_exist(local_root_dir)

    def load_photos(self, photo_dir_name):
        # Call the Drive v3 API
        results = self._fetch_drive_dir()
        items = results.get('files', [])
        root_photo_dir = None
        if not items:
            print('No files found.')
        else:
            print('Files:')
            photo_dir_list = list(
                filter(lambda it: it['name'] == photo_dir_name, items))
            if len(photo_dir_list) > 0:
                root_photo_dir = photo_dir_list[0]

        if root_photo_dir is None:
            raise ValueError('{} directory does not exist on google drive'.format(photo_dir_name))
        else:
            photo_dirs = self._create_local_photo_dirs(root_photo_dir)
            print(photo_dirs)
            self._download_photos_for_dirs(photo_dirs)

    def _create_local_photo_dirs(self, root_photo_dir):
        q="'{0}' in parents".format(root_photo_dir['id'])

        results = self._fetch_drive_dir(q)
        results = list(filter(lambda it: _filter_non_photos(it), results.get('files', [])))

        for rs in results:
            create_folder_if_not_exist('{0}/{1}'.format(self.local_root_dir, rs['name']))
        
        return list(map(
            lambda rs: {'local_path': '{0}/{1}'.format(self.local_root_dir, rs['name']), 'id': rs['id']}, results))

    def _fetch_drive_dir(self, q = None):
        results=None
        if(not q):
            results=self.service.files().list(
                pageSize = self.pageSize, fields = "nextPageToken, files(id, name)").execute()
        else:
            results=self.service.files().list(pageSize=self.pageSize, q = q).execute()
        return results

    def _download_photos_for_dirs(self, photo_dirs):
        for pd in photo_dirs:
            local_path = pd['local_path']
            dir_id = pd['id']
            q = "'{0}' in parents".format(dir_id)
            photo_files = self.service.files().list(pageSize=self.pageSize, q=q).execute()
            photo_files = list(
                filter(lambda it: _filter_non_photos(it), photo_files.get('files', [])))
            for pf in photo_files:
                file_id = pf['id']
                file_name = pf['name']
                request = self.service.files().get_media(fileId=file_id)
                fh = io.FileIO('{0}/{1}'.format(local_path, file_name), 'wb')
                print('Downloading file {0} into {1}'.format(file_id, fh.name))
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print('Download %d%%.' % int(status.progress() * 100))
