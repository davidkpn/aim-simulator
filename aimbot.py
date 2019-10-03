import os
import cv2
import numpy as np
import tensorflow as tf
import sys
sys.path.append("..")

from utils import label_map_util
from utils import visualization_utils as vis_util
import subprocess
subprocess.run("set PYTHONPATH=C:/tensorflow1/models;C:/tensorflow1/models/research;C:/tensorflow1/models/research/slim", shell=True, stdout=subprocess.PIPE)

from mss import mss
from PIL import Image
import win32api, win32con, time


class AimBot:
    # screen settings
    width=1024
    height=768
    bbox_w = int(width/3)
    bbox_h = int(height/3)
    bbox = {"top": bbox_h, "left":  bbox_w, "width":  bbox_w, "height": bbox_h}
    sct = mss()
    # data settings
    MODEL_NAME='inference_graph'
    NUM_CLASSES=4
    CWD_PATH = os.getcwd()
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')
    # Load the label map.
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    # Load the Tensorflow model into memory.
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

        sess = tf.Session(graph=detection_graph)

    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')


    def __init__(self):
        pass

    def run_aimbot(cls, ct, t, *args):
        class_num = 1 if t else 2
        second_frame = True
        while True:
            start = time.time()
            image = AimBot.sct.grab(AimBot.bbox)
            frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
            frame_expanded = np.expand_dims(frame, axis=0)
            if second_frame:
                (boxes, scores, classes, num) = AimBot.sess.run(
                    [AimBot.detection_boxes, AimBot.detection_scores, AimBot.detection_classes, AimBot.num_detections],
                    feed_dict={AimBot.image_tensor: frame_expanded})
                second_frame = False
                end = time.time()
                print(2/(end - start))
                for i in range(len(scores)):
                    if scores[0][i] > 0.9:
                        if classes[0][i] == class_num:
                            ymin, xmin, ymax, xmax = boxes[0][i]
                            x_delta, y_delta = int((xmax+xmin-1)*AimBot.bbox_w/2), int((ymin+ymax-1)*AimBot.bbox_h/2)
                            if (xmax-xmin)*AimBot.bbox_w > 15 and (ymax-ymin)*AimBot.bbox_h > 10 and xmin < 0.9:
                                AimBot.click(x_delta, y_delta)
                    else:
                        break
                else:
                    continue    

            else:
                second_frame = True
                for i in range(len(scores)):
                    if scores[0][i] > 0.9:
                        if classes[0][i] == class_num:
                            ymin, xmin, ymax, xmax = boxes[0][i]
                            x_delta, y_delta = int((xmax+xmin-1)*AimBot.bbox_w/2), int((ymin+ymax-1)*AimBot.bbox_h/2)
                            if (xmax-xmin)*AimBot.bbox_w > 15 and (ymax-ymin)*AimBot.bbox_h > 10 and xmin < 0.9:
                                AimBot.move(x_delta, y_delta)

            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                AimBot.category_index,
                use_normalized_coordinates=True,
                line_thickness=6,
                min_score_thresh=0.90)
            cv2.imshow('Object detector', frame)
            # Press 'q' to quit
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()

    def click(x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    def move(x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
