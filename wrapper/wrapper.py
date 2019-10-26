from wrapper.logging import dictConfig
import logging
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from keras.applications import ResNet50, imagenet_utils
from keras.preprocessing.image import img_to_array
from keras import backend as K



def create_app():

    app = Flask(__name__)
    model = ResNet50(weights="imagenet")

    def prepare_image(image, target=(224, 224)):
        logging.debug("prepare_image is running")
        # if the image mode is not RGB, convert it
        if image.mode != "RGB":
            image = image.convert("RGB")

        # resize the input image and preprocess it
        image = image.resize(target)
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        image = imagenet_utils.preprocess_input(image)

        # return the processed image
        return image

    def pred(new_image):
        logging.debug("main is running")
        image = Image.open(new_image)
        image = prepare_image(image)
        preds = model.predict(image)
        results = imagenet_utils.decode_predictions(preds)
        return str(results)



    @app.route('/predict', methods=['POST'])
    def predict():
        logging.info("/predict request")
        if len(request.files) != 1:
            return jsonify({"error": f"expected 1 file attached, received {len(request.files)}"}), 400
        if 'file' not in request.files:
            return jsonify({"error": "parameter 'file' not found in request body"}), 400
        try:
            Image.open(request.files['file'])
        except IOError as e:
            return jsonify({"error": "wrong attached file format, image cannot be opened and identified"}), 400
        logging.debug("all the conditions are met, passing image to main")
        return jsonify({"prediction": pred(request.files['file'])}), 200

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"health": "OK"}), 200

    return app


