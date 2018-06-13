import os

def create_folder_if_not_exist(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
