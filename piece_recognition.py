import os
import re
import numpy as np
import pandas as pd
import sklearn
import tensorflow as tf
import tensorflow.python.platform
import matplotlib.pyplot as plt
import pickle
import cv2

from scipy.ndimage import imread
from tensorflow.python.platform import gfile
from tensorflow.contrib import learn
from sklearn.model_selection import cross_validate
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.svm import SVC, LinearSVC
from IPython.core.display import Image, display

# creates graph from Inception, loads it in 
def create_graph():
  #loading in classify_image_graph_def.pb
  with gfile.FastGFile("classify_image_graph_def.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')


# extract the deep features in the last layer of the inception model. 
# input: a list of images
# output: list of deep features
def extract_deep_features(list_images):
    feature_num = 2048 #number of deep features per image
    image_num = len(list_images) #number of images to process
    features = np.empty((image_num , feature_num)) # Deep Features to be stored here
    create_graph() # Create a TensorFlow computation graph
    with tf.Session() as s:
        next_to_last_tensor = s.graph.get_tensor_by_name('pool_3:0') 
        for ind, image_data in enumerate(list_images):
            print(image_data)
            predictions = s.run(next_to_last_tensor,
                                {'DecodeJpeg/contents:0': image_data})
            features[ind,:] = np.squeeze(predictions)
    print('')
    print('Done!')
    return features

# Makes predictions given a list of deep features
# outputs a list of numbers corresponding to a piece. See CATEGORIES for corresponding index
def make_prediction(features, model_directory):
    n_classes = 13
    feature_columns = [tf.contrib.layers.real_valued_column("", dimension=2048)]

    loaded_model = learn.LinearClassifier(feature_columns = 
                            feature_columns, n_classes= n_classes, model_dir=model_directory)

    new_label_predicted = list(loaded_model.predict(features))
    return new_label_predicted

#load in images as arrays
def load_images(images):
    image_list = []
    for x in images:
        # openCVImage = cv2.imread(x)
        image_to_list = cv2.imencode('.jpg', x)[1].tostring()
        image_list.append(image_to_list)
    return image_list

def recognise_pieces(squares):
    CATEGORIES = ["bb", "bk", "bn", "bp", "bq", "br", "empty", "wb", "wk", "wn", "wp", "wq", "wr"]
    image_list = load_images(squares)
    print("image data loaded")
    features = extract_deep_features(image_list)
    print("Deep features extracted")
    model_directory = "/model/final-model" # directory to saved model
    pieces = make_prediction(features, model_directory)
    return pieces, CATEGORIES


