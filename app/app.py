import base64
from io import BytesIO
import numpy as np
from ml import predict_utils
from PIL import Image
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

size = [64,64]

bp = Blueprint('app', __name__, url_prefix='/')
    
@bp.route('/', methods = ['GET'])
def draw_base():
    return render_template('draw.html')

@bp.route('/_predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        draw = request.get_json()
        draw = draw[22:]
        draw_decode = base64.b64decode(draw)
        
        #Get ndarray and make it grey scale
        image = Image.open(BytesIO(draw_decode)).convert('RGBA')
        image = np.array(image)
        red, green, blue, alpha = image.T

        black_areas = (red==0) & (blue == 0) & (green == 0) & (alpha != 0)
        image[..., :-1][black_areas.T] = (255, 255, 255)

        image = Image.fromarray(image).convert('L')

        # resize the image
        image = image.resize((size[0], size[1]), Image.ANTIALIAS)
        vect = np.asarray(image, dtype='uint8')
        vect = (vect.flatten())
        vect = vect.reshape(1, size[0], size[1])

        final_pred, conf = predict_utils.predict(vect, from_cloud=True)
    
        for i in range(5):
            conf[i] += ": " + final_pred[i]

    return jsonify({'result':final_pred[0], 'top_five': conf})
