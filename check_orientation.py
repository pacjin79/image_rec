import face_recognition as fc
from os import path
from PIL import Image, ImageDraw
import numpy

image_path = path.join('photo_processed', 'Colosus', 'FJZ_2624_mod_.JPG')

rotated = Image.open(image_path).rotate(90)

source_img = numpy.array(rotated)

# fc.load_image_file(image_path)
locations = fc.face_locations(source_img,  number_of_times_to_upsample=1, model='cnn')
# encodings = fc.face_encodings(source_img, locations)
face_landmarks_list = fc.face_landmarks(source_img, locations)


print(face_landmarks_list)
for face_landmarks in face_landmarks_list:
    pil_img = Image.fromarray(source_img)
    draw = ImageDraw.Draw(pil_img)
     # Make the eyebrows into a nightmare
    draw.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
    draw.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
    draw.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=5)
    draw.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=5)

     # Gloss the lips
    draw.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
    draw.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
    draw.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=8)
    draw.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=8)

    pil_img.show()