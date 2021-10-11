from re import L
import tensorflow.keras as k
import tensorflow as tf
import os
import numpy as np
import pandas as pd
from pathlib import Path

PATH_TO_ROOT = Path(__file__).parent.parent
model = k.models.load_model(os.path.join(PATH_TO_ROOT, 'ml', 'models', 'final_model'))

def predict(X):
    """
    Input: unscailed 1 x 28 x 28 matrix of grey scailed images.
    Output: a classified Japanese characters corresponding to the input.
    """
    # X data need to be shaped correctly
    if X.shape[1:] == [28, 28]:
        raise Exception("Shape of X needs to be of (#, 28, 28)")
    
    X = X/255.0

    character = model.predict(X.reshape(1, 28, 28, 1))

    label_df = pd.read_csv(
        os.path.join(PATH_TO_ROOT, 'ml', 'datasets', 'k49_classmap.csv')
    )

    # remove the characters from labels.
    label_df = label_df.drop([44, 45, 48])
    label_df.reset_index(drop=True)
    label_df['index'] = label_df.index

    return label_df['char'][np.argmax(character, axis=1)].tolist()[0]


if __name__ == "__main__":
    pass
