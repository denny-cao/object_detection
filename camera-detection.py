import numpy as np 
import os 
import six.moves.urllib as urllib 
import sys 
import tarfile 
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import zipfile 
import tkinter 
from collections import defaultdict 
from io import StringIO 
from matplotlib import pyplot as plt 
from PIL import Image 

import cv2 
cap = cv2.VideoCapture(0) 

sys.path.append("..") 
import sys
if r"C:\\Users\Denny\Downloads\models\research" not in sys.path:
    sys.path.append(r"C:\\Users\Denny\Downloads\models\research")

from object_detection.utils import label_map_util

from object_detection.utils import visualization_utils as vis_util

def reconstruct(pb_path):
    if not os.path.isfile(pb_path):
        print("Error: %s not found" % pb_path)

    print("Reconstructing Tensorflow model")
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(pb_path, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    print("Success!")
    return detection_graph

MODEL_NAME = 'ssd_mobilenet_v2_taco_2018_03_29' 

# Path to frozen detection graph. This is the actual model that is used for the object detection. 
PATH_TO_CKPT = MODEL_NAME + '/model.pb' 

# List of the strings that is used to add correct label for each box. 
PATH_TO_LABELS = MODEL_NAME + '/labelmap.pbtxt'

NUM_CLASSES = 60

detection_graph = reconstruct(PATH_TO_CKPT)

label_map = label_map_util.load_labelmap(PATH_TO_LABELS) 
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True) 
category_index = label_map_util.create_category_index(categories) 

with detection_graph.as_default(): 
    with tf.Session(graph=detection_graph) as sess: 
        while True: 
            ret, image_np = cap.read() 
            image_np_expanded = np.expand_dims(image_np, axis=0) 
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0') 
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0') 
            # Score is shown on the result image, together with class label. 
            scores = detection_graph.get_tensor_by_name('detection_scores:0') 
            classes = detection_graph.get_tensor_by_name('detection_classes:0') 
            num_detections = detection_graph.get_tensor_by_name('num_detections:0') 

            # Actual detection. 
            (boxes, scores, classes, num_detections) = sess.run( 
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded}) 
            # Visualization of the results of a detection. 
            vis_util.visualize_boxes_and_labels_on_image_array( 
                    image_np,
                    np.squeeze(boxes),
                    np.squeeze(classes).astype(np.int32),
                    np.squeeze(scores),
                    category_index,
                    use_normalized_coordinates=True,
                    line_thickness=8) 

            cv2.imshow('object detection', cv2.resize(image_np, (800,600))) 
            if cv2.waitKey(25) == ord('q'): 
                cv2.destroyAllWindows() 
                break 
