from helpers.google_drive_helper import GoogleDriveHelper

local_photo_root_dir = 'photos'
photo_dir_name = 'Leo Test'
gdrive_helper = GoogleDriveHelper(local_photo_root_dir)

try:
    gdrive_helper.load_photos(photo_dir_name)
except ValueError:
    raise
