import os
import numpy as np
import pandas as pd
from pathlib import Path

PATH_TO_ROOT = Path(__file__).parent.parent
size = [64, 64]

def predict(X, from_cloud=False):
    """
    Input: unscailed 1 x 64 x 64 matrix of grey scailed images.
    Output: top 5 classified labels and associated confidence %
    """

    X = preprocess(X)

    if from_cloud == True:
        from sagemaker import Session
        from sagemaker.tensorflow import TensorFlowPredictor

        model = TensorFlowPredictor('inference-hiragana')
            
        predictions = np.array(model.predict(X)['predictions'])
    else :
        import tensorflow.keras as k
        import tensorflow as tf
        model = k.models.load_model(os.path.join(PATH_TO_ROOT, 'ml', 'models', 'final_model'))
        predictions = model.predict(X)

    return get_top5(predictions)


def preprocess(X):
    # X data need to be shaped correctly
    if X.shape[1:] != (64, 64):
        raise Exception("Shape of X needs to be of (#, 64, 64)")

    X = X/255.0
    X = X.reshape(1, size[0], size[1], 1)
    return X

def get_top5(predictions):
    label_df = pd.read_csv(
        os.path.join(PATH_TO_ROOT, 'ml', 'datasets', 'hiragana.csv')
    )

    ind = np.argpartition(predictions[0], -5)[-5:]
    hiragana = label_df['character'][ind[np.argsort(predictions[0][ind])][::-1]].tolist()
    confidence = predictions[0][ind[np.argsort(predictions[0][ind])][::-1]]

    return list(hiragana), ['{:.2f}%'.format(i * 100) for i in confidence]

if __name__ == "__main__":
    pass
