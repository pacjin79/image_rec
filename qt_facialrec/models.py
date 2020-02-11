import numpy as np
import cv2
import face_recognition

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.last_frame = np.zeros((1,1))

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        # load known faces
        leo_image = face_recognition.load_image_file("./photo_processed/leo_photos/leo_1.png")
        leo_face_encoding = face_recognition.face_encodings(leo_image)[0]
        vineet_image = face_recognition.load_image_file("./photo_processed/vineet_photos/vineet_1.jpg")
        vineet_face_encoding = face_recognition.face_encodings(vineet_image)[0]
        adrianna_image = face_recognition.load_image_file("./photo_processed/vineet_photos/Adriana.jpg")
        adrianna_face_encoding = face_recognition.face_encodings(adrianna_image)[0]
        gail_image = face_recognition.load_image_file("./photo_processed/vineet_photos/gail.jpg")
        gail_face_encoding = face_recognition.face_encodings(gail_image)[0]
        amanda_image = face_recognition.load_image_file("./photo_processed/vineet_photos/Amanda.jpg")
        amanda_face_encoding = face_recognition.face_encodings(amanda_image)[0]
        
        self.known_face_encodings = [
            leo_face_encoding,
            vineet_face_encoding,
            adrianna_face_encoding,
            gail_face_encoding,
            amanda_face_encoding
        ]
        self.known_face_names = [
            'Leo',
            "Vineet",
            "Adriana",
            "Gail"
            "Amanda"
        ]
        self.known_face_titles = [
            "Alpha Labs Leader",
            "Digital Venture Leader",
            "Strategic Initiatives Leader",
            "Chief Digital Officer"
        ]
        self.known_face_locations = [
            "New York City",
            "New York City",
            "New York City",
            "New York City",
            "New York City"
        ]
        self.known_face_emails = [
            "leo.jin@mercer.com",
            "vineet.malhotra@mercer.com",
            "adriana.xxx@mercer.com",
            "gail.evans@mercer.com",
            "amanda.xxx@mercer.com"
        ]

    def get_frame(self):
        ret, self.last_frame = self.cap.read()
        return self.last_frame

    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            movie.append(self.get_frame())
        return movie

    def get_frame_with_face_rec(self):
        frame = self.get_frame()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = self.recognize_faces(frame)
        return frame

    def recognize_faces(self, frame):
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = []
        face_encodings = []
        face_names = []

        # Only process every other frame of video to save time
        # if self.process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
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
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                face_info['name'] = self.known_face_names[best_match_index]
                face_info['title'] = self.known_face_titles[best_match_index]
                face_info['location'] = self.known_face_locations[best_match_index]
                face_info['email'] = self.known_face_emails[best_match_index]
            face_names.append(face_info)

        # self.process_this_frame = not self.process_this_frame
        # Display the results
        for (top, right, bottom, left), face_info in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (230, 104, 0), 0)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom + 150), (right, bottom), (230, 104, 0), 0)
            font = cv2.FONT_HERSHEY_TRIPLEX
            # print('length = ', right - left)
            cv2.putText(frame, face_info['name'], (left + 20, bottom + 32), font, 1.0, (255, 255, 255), 2)
            cv2.putText(frame, face_info['title'], (left + 20, bottom + 64), font, 0.65, (255, 255, 255), 1)
            cv2.putText(frame, face_info['location'], (left + 20, bottom + 96), font, 0.65, (255, 255, 255), 1)
            cv2.putText(frame, face_info['email'], (left + 20, bottom + 128), font, 0.5, (255, 255, 255), 1)
        
        return frame

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def close_camera(self):
        self.cap.release()

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)


if __name__ == '__main__':
    cam = Camera(0)
    cam.initialize()
    print(cam)
    frame = cam.get_frame()
    print(frame)
    cam.set_brightness(1)
    print(cam.get_brightness())
    cam.set_brightness(0.5)
    print(cam.get_brightness())
    cam.close_camera()