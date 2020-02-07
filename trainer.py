import cv2
import os
import numpy as np
from PIL import Image
import sys
import glob

path = os.path.dirname(os.path.abspath(__file__))
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
dataPath = path+r'\dataSet'

def get_images_and_labels(datapath):
     image_paths = [os.path.join(datapath, f) for f in os.listdir(datapath)]
     print(image_paths)
     # images will contains face images
     images = []
     # labels will contains the label that is assigned to the image
     labels = []
     for image_path in image_paths:
         for img in glob.glob(image_path+r'/*.png'):
             # Read the image and convert to grayscale
             image_pil = Image.open(img).convert('L')
             # Convert the image format into numpy array
             image = np.array(image_pil, 'uint8')
             # Get the label of the image
             nbr = int(os.path.split(img)[1].split(".")[0].replace("face-", ""))
             #nbr=int(''.join(str(ord(c)) for c in nbr))
             print(nbr)
             # Detect the face in the image
             faces = face_cascade.detectMultiScale(image)
             # If face is detected, append the face to images and the label to labels
             for (x, y, w, h) in faces:
                 images.append(image[y: y + h, x: x + w])
                 labels.append(nbr)
                 cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
                 cv2.waitKey(10)
     # return the images list and labels list
     return images, labels


images, labels = get_images_and_labels(dataPath)
cv2.imshow('test',images[0])
cv2.waitKey(1)

recognizer.train(images, np.array(labels))
recognizer.save(path+r'\trainer\trainer.yml')
cv2.destroyAllWindows()
