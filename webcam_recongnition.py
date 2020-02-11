import face_recognition
import cv2
import numpy as np

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

mf_image = face_recognition.load_image_file("mf.png")
mf_face_encoding = face_recognition.face_encodings(mf_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

leo_image = face_recognition.load_image_file("./photo_processed/leo_photos/leo_1.png")
leo_face_encoding = face_recognition.face_encodings(leo_image)[0]

nancy_image = face_recognition.load_image_file("./photo_processed/leo_photos/nancy_1.png")
nancy_face_encoding = face_recognition.face_encodings(nancy_image)[0]

vineet_image = face_recognition.load_image_file("./photo_processed/vineet_photos/vineet_1.jpg")
vineet_face_encoding = face_recognition.face_encodings(vineet_image)[0]

adrianna_image = face_recognition.load_image_file("./photo_processed/vineet_photos/Adriana.jpg")
adrianna_face_encoding = face_recognition.face_encodings(adrianna_image)[0]

gail_image = face_recognition.load_image_file("./photo_processed/vineet_photos/gail.jpg")
gail_face_encoding = face_recognition.face_encodings(gail_image)[0]

amanda_image = face_recognition.load_image_file("./photo_processed/vineet_photos/Amanda.jpg")
amanda_face_encoding = face_recognition.face_encodings(amanda_image)[0]

bala_image = face_recognition.load_image_file("./el-photos/bala-viswanathan.jpg")
bala_face_encoding = face_recognition.face_encodings(bala_image)[0]

balzano_image = face_recognition.load_image_file("./el-photos/balzano-herve.jpg")
balzano_face_encoding = face_recognition.face_encodings(balzano_image)[0]

david_image = face_recognition.load_image_file("./el-photos/david-anderson-300x300.jpg")
david_face_encoding = face_recognition.face_encodings(david_image)[0]

# gail_image = face_recognition.load_image_file("./el-photos/gail-evans-600x600.jpg")
# gail_face_encoding = face_recognition.face_encodings(gail_image)[0]

ilya_image = face_recognition.load_image_file("./el-photos/ilya-bonic-300x300.jpg")
ilya_face_encoding = face_recognition.face_encodings(ilya_image)[0]

jackie_image = face_recognition.load_image_file("./el-photos/jackie-marks-600x600.jpg")
jackie_face_encoding = face_recognition.face_encodings(jackie_image)[0]

louis_image = face_recognition.load_image_file("./el-photos/louis-gagnon-600x600.jpg")
louis_face_encoding = face_recognition.face_encodings(louis_image)[0]

marcelo_image = face_recognition.load_image_file("./el-photos/marcelo-modica-600x600.jpg")
marcelo_face_encoding = face_recognition.face_encodings(marcelo_image)[0]

martine_image = face_recognition.load_image_file("./el-photos/martine-ferland-600x600.jpg")
martine_face_encoding = face_recognition.face_encodings(martine_image)[0]

rian_image = face_recognition.load_image_file("./el-photos/rian-miller-300x300.jpg")
rian_face_encoding = face_recognition.face_encodings(rian_image)[0]

rich_image = face_recognition.load_image_file("./el-photos/rich-nuzum-300x300.jpg")
rich_face_encoding = face_recognition.face_encodings(rich_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    leo_face_encoding,
    vineet_face_encoding,
    adrianna_face_encoding,
    gail_face_encoding,
    bala_face_encoding,
    balzano_face_encoding,
    david_face_encoding,
    ilya_face_encoding,
    jackie_face_encoding,
    louis_face_encoding,
    marcelo_face_encoding,
    martine_face_encoding,
    rian_face_encoding,
    rich_face_encoding
]
known_face_names = [
    "Leo",
    "Vineet",
    "Adriana",
    "Gail Evans",
    "Bala Viswanathan",
    "Hervé Balzano",
    "David Anderson",
    "Ilya Bonic",
    "Jackie Marks",
    "Louis Gagnon",
    "Marcelo Modica",
    "Martine Ferland",
    "Rian Miller",
    "Rich Nuzum"
]

known_face_titles = [
    "Alpha Labs Leader",
    "Digital Venture Leader",
    "Strategic Initiatives Leader",
    "Chief Digital Officer",
    "Chief Operating Officer",
    "President, Health",
    "President, International",
    "President, Global Business Solutions and Career",
    "Chief Financial Officer",
    "President, US & Canada",
    "Chief People Officer",
    "President and Chief Executive Officer",
    "Vice President and General Councel",
    "President, Wealth"
]

known_face_locations = [
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City",
    "New York City"
]

known_face_emails = [
    "leo.jin@mercer.com",
    "vineet.malhotra@mercer.com",
    "adriana.xxx@mercer.com",
    "gail.evans@mercer.com",
    "bala.viswanathan@mercer.com",
    "hervé.balzano@mercer.com",
    "david.anderson@mercer.com",
    "ilya.bonic@mercer.com",
    "jackie.marks@mercer.com",
    "louis.gagnon@mercer.com",
    "marcelo.modica@mercer.com",
    "martine.ferland@mercer.com",
    "rian.miller@mercer.com",
    "rich.nuzum@mercer.com"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_info = {
                'name': 'Unknown',
                'title': 'Unknown',
                'location': 'Unknown',
                'email': 'Unknown'
            }

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                face_info['name'] = known_face_names[best_match_index]
                face_info['title'] = known_face_titles[best_match_index]
                face_info['location'] = known_face_locations[best_match_index]
                face_info['email'] = known_face_emails[best_match_index]
            face_names.append(face_info)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), face_info in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (230, 104, 0), 1)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom + 150), (right, bottom), (230, 104, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_TRIPLEX
        cv2.putText(frame, face_info['name'], (left + 20, bottom + 32), font, 1.0, (255, 255, 255), 2)
        
        cv2.putText(frame, face_info['title'], (left + 20, bottom + 64), font, 0.65, (255, 255, 255), 1)
        cv2.putText(frame, face_info['location'], (left + 20, bottom + 96), font, 0.65, (255, 255, 255), 1)
        cv2.putText(frame, face_info['email'], (left + 20, bottom + 128), font, 0.5, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()