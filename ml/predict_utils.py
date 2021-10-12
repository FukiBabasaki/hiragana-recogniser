from re import L
import tensorflow.keras as k
import tensorflow as tf
import os
import numpy as np
import pandas as pd
from pathlib import Path

PATH_TO_ROOT = Path(__file__).parent.parent
model = k.models.load_model(os.path.join(PATH_TO_ROOT, 'ml', 'models', 'final_model'))
size = [64, 64]

def predict(X):
    """
    Input: unscailed 1 x 54 x 64 matrix of grey scailed images.
    Output: a classified Japanese characters corresponding to the input.
    """
    # X data need to be shaped correctly
    if X.shape[1:] == [28, 28]:
        raise Exception("Shape of X needs to be of (#, 28, 28)")
    
    X = X/255.0

    character = model.predict(X.reshape(1, size[0], size[1], 1))

    label_df = pd.read_csv(
        os.path.join(PATH_TO_ROOT, 'ml', 'datasets', 'hiragana.csv')
    )

    # hiragana = label_df['character'][np.argmax(character, axis=1)].tolist()

    ind = np.argpartition(character[0], -5)[-5:]
    hiragana = label_df['character'][ind[np.argsort(character[0][ind])][::-1]].tolist()
    confidence = character[0][ind[np.argsort(character[0][ind])][::-1]]

    return list(hiragana), ['{:.2f}%'.format(i) for i in confidence]


if __name__ == "__main__":
    pass
