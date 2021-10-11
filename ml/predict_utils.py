import tensorflow.keras as k
import os
import numpy as np
from typing import List

def predict(X) -> List[chr]:
    """
    Input: unscailed 1 x 28 x 28 matrix of grey scailed images.
    Output: a classified Japanese characters corresponding to the input.
    """
    # X data need to be shaped correctly
    if X.shape[1:] == [28, 28]:
        raise Exception("Shape of X needs to be of (#, 28, 28)")
    
    model = k.models.load_model(os.path.join('models', 'final_model.h5'))
    character = model.predict(X.reshape(X[0], 28, 28, 1))

    return character[0]


if __name__ == "__main__":
    pass
