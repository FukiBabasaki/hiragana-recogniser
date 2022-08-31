import base64
from io import BytesIO
import numpy as np
from ml import predict_utils
from PIL import Image
import cv2
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

size = [64,64]

bp = Blueprint('app', __name__, url_prefix='/')
    
@bp.route('/', methods = ['GET'])
def draw_base():
    return render_template('draw.html')

@bp.route('/predict', methods=['POST'])
def predict():
    try:
        draw = request.get_json()
        print(draw)
        draw = draw.split(',')[1]
        draw_decode = base64.b64decode(draw)
        
        im_arr = np.frombuffer(draw_decode, dtype=np.uint8)
        print(im_arr)
        image = cv2.imdecode(im_arr, cv2.IMREAD_UNCHANGED)
        print(im_arr.shape)
        cv2.imwrite('test.png', image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        ret,image = cv2.threshold(image,127,255,cv2.THRESH_BINARY)
        
        image = cv2.resize(image, (size[0], size[1]), interpolation=cv2.INTER_AREA)
        vect = np.asarray(image, dtype='uint8')
        vect = (vect.flatten())
        vect = vect.reshape(1, size[0], size[1])

        final_pred, conf = predict_utils.predict(vect)

        # for i in range(5):
        #     conf[i] += ": " + final_pred[i]
        response = jsonify({'result':final_pred[0], 'top_five': conf})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        print(e)
        return jsonify({'error': 'error'})
    
        
