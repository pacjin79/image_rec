import face_recognition
from PIL import Image
import numpy as np
import os
from helpers import io_helper

# list any invalid image directories here to be filtred out
invalid_dirs = ['.DS_Store']
root_processed_photo_dir = 'photo_processed'
recognizable_img_dir = 'photo_recognizable'
unrecognizable_img_dir = 'photo_unrecognizable'
facial_compare_tolerance = 0.52

img_processing_bookkeeping = {}

face_encode_bookkeeping = []


def list_image_dirs(dir=root_processed_photo_dir):
    return list(map(lambda d: os.path.join(dir, d), list(filter(lambda d: d not in invalid_dirs, os.listdir(dir)))))


def get_image_paths_from_dir(dir):
    return list(map(lambda im: os.path.join(dir, im), os.listdir(dir)))


def search_encoding_bookkeeping(source_encoding):
    idx = 0
    for item in face_encode_bookkeeping:
        item_encoding = item['encoding']
        if face_recognition.compare_faces([item_encoding], source_encoding, tolerance=facial_compare_tolerance)[0]:
            return idx
        idx += 1
    return None



def process_image(img_path, sourcePic, model='hog'):
    img_tokens = img_path.split('/')
    img_name_and_ext = os.path.splitext(img_tokens[2])

    try:
        if not img_path in img_processing_bookkeeping:
            img_processing_bookkeeping[img_path] = {
                'rotated': False
            }
        face_locations = face_recognition.face_locations(
            sourcePic, number_of_times_to_upsample=1, model=model)
        faceEncoding = face_recognition.face_encodings(
            sourcePic, face_locations)[0]
        face_idx = search_encoding_bookkeeping(faceEncoding)
        if face_idx is None:
            face_encode_bookkeeping.append({
                'encoding': faceEncoding,
                'same_imgs': [img_path]
            })
        else:
            face_encode_bookkeeping[face_idx]['same_imgs'].append(img_path)
        top, right, bottom, left = face_locations[0]
        face_image_array = sourcePic[top:bottom, left:right]
        face_image = Image.fromarray(face_image_array)
        recognize_img_subdir = os.path.join(
            recognizable_img_dir, img_tokens[1])
        io_helper.create_folder_if_not_exist(recognize_img_subdir)
        recognize_img_path = os.path.join(
            recognize_img_subdir, img_name_and_ext[0] + '_face_' + img_name_and_ext[1])
        face_image.save(recognize_img_path)
        return True
    except IndexError:
        img_rotated = img_processing_bookkeeping[img_path]['rotated']
        if not img_rotated:
            print('not found, rotate and re-evaluate')
            rotated_source_pic = rotate_image_90(sourcePic)
            img_processing_bookkeeping[img_path]['rotated'] = True
            return process_image(img_path, rotated_source_pic, model)
        else:
            print('failed to find faces in photo {0}'.format(img_path))
            unrec_img_subdir = os.path.join(
                unrecognizable_img_dir, img_tokens[1])
            io_helper.create_folder_if_not_exist(unrec_img_subdir)
            unrec_img_path = os.path.join(
                unrec_img_subdir, img_name_and_ext[0] + img_name_and_ext[1])
            Image.fromarray(sourcePic).save(unrec_img_path)
            pass
            return False


def rotate_image_90(img_array):
    img = Image.fromarray(img_array)
    img = img.rotate(90)
    return np.array(img)


def recognize_images(image_paths):
    # cnn or hog
    model = 'hog'

    io_helper.create_folder_if_not_exist(recognizable_img_dir)
    io_helper.create_folder_if_not_exist(unrecognizable_img_dir)

    total_image_count = len(image_paths)
    image_processed = 0
    image_processed_success = 0
    image_processed_fail = 0

    print('total images to process: {0}'.format(total_image_count))
    for img_path in image_paths:
        sourcePic = face_recognition.load_image_file(img_path)
        process_success = process_image(img_path, sourcePic, model=model)
        if process_success:
            image_processed_success += 1
        else:
            image_processed_fail += 1
        image_processed += 1
        print('completed {0}%'.format(image_processed/total_image_count * 100))

    for idx, photo_item in enumerate(face_encode_bookkeeping):
        print(str(idx)+'! same_img = ' + str(photo_item['same_imgs']))
        category_dir = os.path.join(recognizable_img_dir, 'category_' + str(idx))
        io_helper.create_folder_if_not_exist(category_dir)
        rec_img_paths = photo_item['same_imgs']
        for rimg in rec_img_paths:
            Image.open(rimg).save(os.path.join(category_dir, rimg.split('/')[2]))

    print('All photos processed with a success rate of {0}%, with {1} number of success and {2} number of failure'
          .format(image_processed_success / total_image_count * 100, image_processed_success, image_processed_fail))


def main():
    image_dirs = list_image_dirs()
    for d in image_dirs:
        image_paths = get_image_paths_from_dir(d)
        # todo: remove later, only filtering for testing purposes
        if(d.startswith('photo_processed/Combo')):
            recognize_images(image_paths)


main()