from flask import render_template, session, redirect, url_for, request, g, send_from_directory
from app import webapp

import mysql.connector

from app.config import db_config

import cv2
from random import randint

import os

webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f\xee'

PICLIST_SIZE = 8

def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@webapp.route('/images/upload', methods=['POST'])
# upload new images and save their filepaths in the database.
def images_upload():

    user_id = session.get('username')

    ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images', str(user_id))

    cnx = get_db()
    cursor = cnx.cursor()
    query = '''SELECT image_name FROM user_has_images
                                  WHERE user_id = %s'''
    cursor.execute(query, (user_id,))
    row = cursor.fetchall()
    img_saved = []
    for img in row:
        img_saved.append(img)

    flag = True
    #Check if user has already uploaded 100 pictures
    if len(img_saved) >= PICLIST_SIZE:
        flag = False

    if flag == True:
        for upload in request.files.getlist("file"):
            filepath = upload.filename
            path = os.path.join(ROOT,filepath)
            upload.save(path)

            query1 = ''' INSERT INTO images (filepath) VALUES (%s)'''
            cursor.execute(query1, (filepath,))

            query2 = '''INSERT INTO user_has_images (user_id, image_name) VALUES(%s, %s)'''
            cursor.execute(query2, (user_id, filepath))

            # create thumbnails
            filepath_thumb = filepath + '_thumbnail.png'
            path_thumb_full = os.path.join(ROOT, filepath_thumb)

            # create rotated transformations path
            filepath_detected = filepath+ '_detected.png'
            path_detected_full = os.path.join(ROOT, filepath_detected)

            img = cv2.imread(path)
            #use CV2 to create thumbnail figures
            thumb_nail = img.copy()
            r = 100.0 / thumb_nail.shape[1]
            dim = (100, int(thumb_nail.shape[0] * r))
            maxsize = (128,128)

            # perform the actual resizing of the image and show it
            resized = cv2.resize(thumb_nail, maxsize, interpolation=cv2.INTER_AREA)
            cv2.imwrite(path_thumb_full, resized)
            cv2.waitKey(0)

            #use cv2 to detect face and save in folder
            classifier_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')
            face_cascade = cv2.CascadeClassifier(classifier_path)
            detect = img.copy()
            gray = cv2.cvtColor(detect, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            # Draw a rectangle around the faces
            if len(faces) != 0:
                for (x, y, w, h) in faces:
                        cv2.rectangle(detect, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imwrite(path_detected_full, detect)
            else:
                msg = 'No face detected in the picture!'
            cv2.destroyAllWindows()

    cnx.commit()

    return redirect(url_for('user_home', flag=flag))


@webapp.route('/images/trans/<filepath>', methods=['GET'])
# show the transformations of a specific image.
def images_trans(filepath):
    if 'authenticated' not in session:
        return redirect(url_for('login'))

    return render_template("images/trans.html",title="Transformations", filepath=filepath)


@webapp.route('/trans/<filepath>', methods=['GET','POST'])
# display thumbnails of a specific account
def send_image_trans(filepath):
    user_id = session.get('username')
    path = os.path.join('images', str(user_id))

    return send_from_directory(path, filepath)


@webapp.route('/', methods=['POST'])
def auto_upload():
    user_id = session.get('username')

    cnx = get_db()
    cursor = cnx.cursor()
    abspath = "/Users/yisheng/Developer/Github/AnswerTea/A1/app/"

    query = '''SELECT image_name FROM user_has_images
                              WHERE user_id = %s'''
    cursor.execute(query, (user_id,))

    row = cursor.fetchall()
    img_saved = []
    for img in row:
        img_saved.append(img)

    repeat = True
    flag = True
    while repeat == True:
        if len(img_saved) >= PICLIST_SIZE:
            repeat = False
            flag = False
            break
        gen_id = randint(0, PICLIST_SIZE)
        test_image_name = 'test' + str(gen_id) + '.jpg'  # test1.jpg
        if any (test_image_name in s for s in img_saved):
            # random img id already exist
            repeat = True
        else:
            repeat = False

    if flag==True:
        test_image_path = abspath + 'test_images/' + test_image_name

        img = cv2.imread(test_image_path)

        ROOT = os.path.join(abspath, 'images', str(user_id))
        path = os.path.join(ROOT, test_image_name)

        print('Auto file name:' + test_image_name + '\n')
        print('Auto file Path: ' + test_image_path + '\n')
        print('Auto root: '+ ROOT + '\n')
        print('Auto save file path: ' + path + '\n')

        cv2.imwrite(path, img)

        create_thumbnail(test_image_path, test_image_name, ROOT)

        filepath = test_image_name

        query1 = ''' INSERT INTO images (filepath) VALUES (%s)'''
        cursor.execute(query1, (filepath,))

        query2 = "INSERT INTO user_has_images (user_id, image_name) VALUE(%s, %s)"
        cursor.execute(query2, (user_id, filepath))

    cnx.commit()
    cnx.close()

    return redirect(url_for('user_home', flag=flag))

def create_thumbnail(test_image_path, test_image_name, ROOT):

    filepath_thumb = test_image_name + '_thumbnail.png'
    path_thumb_full = os.path.join(ROOT, filepath_thumb)

    # create rotated transformations path
    filepath_detected = test_image_name + '_detected.png'
    path_detected_full = os.path.join(ROOT, filepath_detected)

    # use CV2 to create thumbnail figures
    img = cv2.imread(test_image_path)
    thumb_nail = img.copy()
    r = 100.0 / thumb_nail.shape[1]
    dim = (100, int(thumb_nail.shape[0] * r))
    maxsize = (128, 128)

    # perform the actual resizing of the image and show it
    resized = cv2.resize(thumb_nail, maxsize, interpolation=cv2.INTER_AREA)
    cv2.imwrite(path_thumb_full, resized)
    cv2.waitKey(0)

    # use cv2 to detect face and save in folder
    classifier_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(classifier_path)
    detect = img.copy()
    gray = cv2.cvtColor(detect, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw a rectangle around the faces
    if len(faces) != 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(detect, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imwrite(path_detected_full, detect)
    else:
        msg = 'No face detected in the picture!'
    cv2.destroyAllWindows()