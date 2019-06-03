import cv2
import os
import numpy as np
#from . import models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#there is no label 0 in our training data so subject name for index/label 0 is empty
#subjects = ["", "Bil Gates", "Steve Jobs"]

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(os.path.join(BASE_DIR, 'find/data/haarcascade_frontalface_alt.xml'))
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    if (len(faces) == 0):
        return None,None

    (x,y,w,h) = faces[0]

    return gray[y:y+w, x:x+h], faces[0]

#data preparation
#this function will read all person's training images, detect face from each image
#and will return two lists of exactly same size, one list of faces
# and another list of labels for each face
def prepare_training_data(data_folder_path):
    #------------STEP 1------------#
    #get the directories (one directory for each subject) in data folder
    subject_dir_path = os.listdir(data_folder_path)

    faces = []
    labels =[]

    for image_name in subject_dir_path:
            #ignore system file like .DS_store
        if image_name.startswith('1'):
            #continue

            #print(image_name)
            label = int(image_name.replace(image_name[image_name.find("."):], ''))
            image_path = data_folder_path + "/" + image_name
                #read image
            print(image_path)
            image = cv2.imread(image_path)

            face, rect = detect_face(image)

                #---------STEP 4-----------#
                #for the purpose of this tutorial
                #we will ignore faces that are not detected
            if face is not None:
                faces.append(face)
                labels.append(label)

            cv2.destroyAllWindows()
            #cv2.waitKey(1)
            cv2.destroyAllWindows()
    return faces, labels

#print("Preparing data ...")
# faces, labels = prepare_training_data("data")
#print("Data prepared")
#print("Total faces: ", len(faces))
#print("Total labels: ", len(labels))


#train face recognizer
#1.EigenFces: cv2.face.createEigenFaceRecognizer()
#2. FisherFces: cv2.face.createFisherFceRecognize()
#3. Local Binary Pattern Histogram (LBPH): cv2.face.LBPHFisherFaceRecognizer()

#create LBPH face recognozer
# face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# #train our face recognizer of our training faces
# face_recognizer.train(faces, np.array(labels))

#function to draw rectrangle on image
#according to given (x,y) coordinates and
#given width and heigh
def draw_rectangle(img, rect):
    (x,y,w,h) = rect
    cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

#function to draw text on give image starting from
#passed (x,y) coordinates
def draw_text(img, text, x, y):
    cv2.putText(img, text,(x,y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,255,0), 2)

#this function recognizes the person in image passed
#and draws a rectangle around detected face with name of the sublect
    
def predict(test_img, face_recognizer):
    img = test_img.copy()
    face,rect = detect_face(img)
    label = face_recognizer.predict(face)
    #label_text = subjects[label[0]]
    #draw_rectangle(img,rect)
    #draw_text(img, label_text, rect[0], rect[1]-5)
    return str(label[0])



def recog(img_path,train_path):
    faces, labels = prepare_training_data(train_path)
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))
    img_path = str(img_path)
    img = cv2.imread(img_path)
    id = predict(img, face_recognizer)
    return id


