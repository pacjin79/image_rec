import os
from PIL import Image
from helpers.io_helper import create_folder_if_not_exist


def map_photo_path(photo_dir):
    path = 'photos/{}'.format(photo_dir)
    results = {
        'photo_dir': photo_dir,
        'images': []
    }
    if os.path.isdir(path):
        photo_list = os.listdir(path)
        results['images'] = list(
            map(lambda ph: '{0}/{1}'.format(path, ph), photo_list))

    return results


def resize_images(file_batch, dest_root_dir):
    photo_dir = file_batch['photo_dir']
    images = file_batch['images']
    dest_dir = '{0}/{1}'.format(dest_root_dir, photo_dir)
    create_folder_if_not_exist(dest_dir)
    scale = 1000
    for img_path in images:
        img = Image.open(img_path)
        img_labels = os.path.splitext(img.filename.lstrip('photos/'))
        img_path = '{0}/{1}{2}'.format(dest_root_dir, img_labels[0] + '_mod_', img_labels[1])
        img_size = (img.size[0] - scale if img.size[0] > scale else img.size[0], img.size[1] - scale if img.size[1] > scale else img.size[1])
        img.thumbnail(img_size)
        img.save(img_path)
        print ('Processed {0} and saved to {1}'.format(img_labels[0], img_path))


def main():
    processed_dir = 'photo_processed'
    create_folder_if_not_exist(processed_dir)
    file_batches = list(map(lambda p: map_photo_path(p), os.listdir('photos')))
    for fb in file_batches:
        resize_images(fb, processed_dir)
        
main()
