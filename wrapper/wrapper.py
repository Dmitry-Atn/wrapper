import numpy as np
from keras.applications import ResNet50, imagenet_utils
from keras.preprocessing.image import img_to_array
from PIL import Image
from flask import Flask, request, jsonify
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

def prepare_image(image, target=(224, 224)):
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

def main(new_image):
    image = Image.open(new_image)
    image = prepare_image(image)

    model = ResNet50(weights="imagenet")
    preds = model.predict(image)

    results = imagenet_utils.decode_predictions(preds)
    return str(results)


def create_app():


    app = Flask(__name__)

    @app.route('/predict', methods=['POST'])
    def predict():
        if len(request.files) != 1:
            return jsonify({"error": f"expected 1 file attached, received {len(request.files)}"}), 400
        if 'file' not in request.files:
            return jsonify({"error": "parameter 'file' not found in request body"}), 400
        try:
            Image.open(request.files['file'])
        except IOError as e:
            return jsonify({"error": "wrong attached file format, image cannot be opened and identified"}), 400
        return jsonify({"prediction": main(request.files['file'])}), 200

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"health": "OK"}), 200

    return app


