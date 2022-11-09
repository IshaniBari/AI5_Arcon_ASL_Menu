import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.python.keras import backend as K
from tensorflow.keras.models import Model
import tensorflow_hub as hub


AUTOTUNE = tf.data.experimental.AUTOTUNE
local_experiments_path = "/persistent"
best_model = "Best_Model.h5"
best_model_id = None
prediction_model = None
data_details = None
image_width = 256
image_height = 256
num_channels = 3
mappings = {0: 'A',1: 'B',2: 'C',3: 'D',4: 'E',5: 'F',6: 'G',7: 'H',8: 'I',9: 'J',10: 'K',11: 'L',12: 'M',13: 'N',14: 'O',15: 'P',16: 'Q',17: 'R',18: 'S',19: 'T',20: 'U',21: 'V',22: 'W',23: 'X',24: 'Y',25: 'Z',26: 'del',27: 'nothing',28: 'space'}

def load_prediction_model():
    print("Loading Model...")
    global prediction_model, data_details

    best_model_path = os.path.join(local_experiments_path,best_model)
    # best_model_path = "/persistent-folder/Best_Model.h5"

    print("best_model_path:", best_model_path)
    prediction_model = tf.keras.models.load_model(
        best_model_path, custom_objects={'KerasLayer': hub.KerasLayer})
    print(prediction_model.summary())



def load_preprocess_image_from_path(image_path):
    print("Image", image_path)

    image_width = 256
    image_height = 256
    num_channels = 3

    # Prepare the data
    def load_image(path):
        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=num_channels)
        image = tf.image.resize(image, [image_height, image_width])
        return image

    # Normalize pixels
    def normalize(image):
        image = image / 255
        return image

    test_data = tf.data.Dataset.from_tensor_slices(([image_path]))
    test_data = test_data.map(load_image, num_parallel_calls=AUTOTUNE)
    test_data = test_data.map(normalize, num_parallel_calls=AUTOTUNE)
    test_data = test_data.repeat(1).batch(1)

    return test_data


def make_prediction(image_path):
    load_prediction_model()
    # Load & preprocess
    test_data = load_preprocess_image_from_path(image_path)

    # Make prediction
    prediction = prediction_model.predict(test_data)
    idx = prediction.argmax(axis=1)[0]
    prediction_label = mappings[idx]

    # Burger = False
    #suggest_menu = None
    if prediction_label == "A":
        suggest_menu = "Aloo Tikki"
    elif prediction_label == "B":
        suggest_menu = "Burger"
    elif prediction_label == "C":
        suggest_menu = "Coca-Cola"
    elif prediction_label == "F":
        suggest_menu = "French fries"
    elif prediction_label == "I":
        suggest_menu = "Ice-cream"
    elif prediction_label == "N":
        suggest_menu = "Noodles"
    elif prediction_label == "R":
        suggest_menu = "Rice Bowl"
    elif prediction_label == "W":
        suggest_menu = "Wrap"
    else: 
        suggest_menu = "No such item available. Please refer menu!"
    

    return {
        "prediction_label": prediction_label,
        "prediction": prediction.tolist(),
        "suggest_menu": suggest_menu
    }
