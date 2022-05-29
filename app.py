from __future__ import division, print_function
import cv2
import face_recognition
import numpy as np
import os
from flask import Flask,flash, redirect, url_for, request, render_template,Response
from werkzeug.utils import secure_filename
from load import * 
from flask import Flask, session
from flask_session import Session   
SESSION_TYPE = 'memcache'

app = Flask(__name__)

sess = Session()
nextId = 0

def verifySessionId():
    global nextId

    if not 'userId' in session:
        session['userId'] = nextId
        nextId += 1
        sessionId = session['userId']
        print ("set userid[" + str(session['userId']) + "]")
    else:
        print ("using already set userid[" + str(session['userId']) + "]")
    sessionId = session.get('userId', None)
    return sessionId

@app.route("/output")
def hello():
    userId = verifySessionId()
    print("User id[" + str(userId) + "]")
    return str(userId)

UPLOAD_FOLDER = '/Users/varnikasingh/data'
ALLOWED_IMAGE_TYPES = set(["png", "jpg", "jpeg", "gif"])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    print("Check if image types is allowed")
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_TYPES


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("test2")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print('upload_image filename: ' + filename)
            return render_template('output.html', filename=filename)
        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')
            return redirect(request.url)

    else:
        return render_template("upload.html")

@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)



camera = cv2.VideoCapture(0)
# Load a sample picture and learn how to recognize it.
image_1 = face_recognition.load_image_file("ragini_33.jpg")       
image_1_encoding = face_recognition.face_encodings(image_1)[0]

# Load a second sample picture and learn how to recognize it.
image_2 = face_recognition.load_image_file("singh_26.jpg")
image_2_encoding = face_recognition.face_encodings(image_2)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    image_1_encoding,
    image_2_encoding
]
known_face_names = [
    "Ragini",
    "Varnika"
]  

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Not A Missing Person"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                face_names.append(name)
            
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/contact')
def contactus():
    return render_template('contact1.html')

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__=='__main__':
    app.secret_key = 'super secret key'

    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run(debug=True)
