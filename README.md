# Japanese Hiragana Recogniser
Handwritten Japanese Hiragana recognition using a deep convolutional neural network. My model follows the framework of [VGGNet](https://arxiv.org/abs/1409.1556) and it performs over 98% accuracy on the test set.

[demo](http://www.fukibabasaki.com/projects/hiragana-recogniser)

This project is inspired by this [thesis](http://cs231n.stanford.edu/reports/2016/pdfs/262_Report.pdf). My model outperforms the score presented in this thesis by around 2-3% in test accuracy thanks to data augmentation and other factors.

## Model Configuration

| Type                     | Size    | Activation |
| ------------------------ | ------- | ---------- |
| Convolution              | 64 x 64 | ReLU       |
| Max Pooling              | 32 x 32 | ReLU       |
| Convolution              | 32 x 32 | ReLU       |
| Convolution              | 32 x 32 | ReLU       |
| Max Pooling              | 16 x 16 | ReLU       |
| Convolution              | 16 x 16 | ReLU       |
| Convolution              | 16 x 16 | ReLU       |
| Max Pooling              | 8 x 8   | ReLU       |
| Fully Connected          | 256     | ReLU       |
| Fully Connected          | 128     | ReLU       |
| Fully Connected (output) | 70      | softmax    |

- Dropout layer is also applied to reduce overfitting.
- Used Adam optimizer with default learning rate and beta values.
- Applied early stopping for when test validation score doesn't improve for 3 epochs in a row.
- Train data are augmented for better generalisation. (applied rotation and zooming)

| Feature           | [Custom Sequential](https://github.com/Fuki-UoA/hiragana-recogniser/blob/main/ml/hiragana-classification.ipynb) | VGGNet | [VGGNet](https://github.com/Fuki-UoA/hiragana-recogniser/blob/main/ml/hiragana-classificationV2.ipynb) |
| ----------------- | ------------------------------------------------------------ | -------- | ------------------------------------------------------------ |
| Test Accuracy     | <= 90%                                                       | <= 98%   | <=  98.88%                                                   |
| Dataset           | Kuzushiji MNIST                                              | ELT-8    | ELT-8                                                        |
| Data Augmentation | No                                                           | No       | Yes                                                          |

Although test accuracy doesn't really differ between model with augmented images and normal images, the performance on predicting user input's character seems to drastically improve. This is partially because the model is more flexible to how the character is written.

## Future work

- The character を is missing from the dataset.
- Further fine-tune the model.
- Feature engieering for stroke order (書き順) and number of strokes (画数).

## Datasets

### Primary

**Dataset**: [ELT-8: ELTDB](http://etlcdb.db.aist.go.jp/specification-of-etl-8)

**Description:** Classification of handwritten Japanese character, 72 classes (五十音順).

**Training & Testing:** 11.5k 128x127 instances.

### Secondary 

**Dataset**: [Kuzushiji MNIST](https://github.com/rois-codh/kmnist)

**Description:** Classification of handwritten Japanese character, 49 classes (五十音順).

**Training:** 232k 28x28 images

**Testing:** 38k 28x28 images

- This dataset did not work well as each instance was only 28 x 28 pixels image and this app takes 400 x 400 pixels image of handwritten Hiragana from the user. Resizing from 400 x 400 to 28 x 28 seems to lose significant amount of information.
- Hence, my model performed reasonably well on the dataset (achieving over 90% accuracy on test set) but performance on the app wasn't great.

## References

Simonyan, Karen, and Andrew Zisserman. "Very deep convolutional networks for large-scale image recognition." arXiv preprint arXiv:1409.1556 (2014).

Tsai, Charlie. "Recognizing handwritten Japanese characters using deep convolutional neural networks." University of Stanford in Stanford, California (2016): 405-410.

森俊二、山本和彦、山田博三、斉藤泰一: “手書教育漢字のデータベースについて”, 「電総研彙報」, Vol.43, Nos.11&12, pp.752–773 (1979-11&12).

"KMNIST Dataset" (created by CODH), adapted from "Kuzushiji Dataset" (created by NIJL and others), doi:10.20676/00000341
