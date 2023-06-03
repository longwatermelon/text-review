import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import text_to_word_sequence
import sys
max_features = 60000
maxlen = 200

model = tf.keras.models.load_model("model.h5")

def predict(sentence):
    tokens = text_to_word_sequence(sentence)

    word_index = imdb.get_word_index()
    tokens_indices = [word_index[token] for token in tokens if token in word_index]

    if len(tokens_indices) == 0:
        return "neutral";

    for i in range(len(tokens_indices)):
        if tokens_indices[i] > max_features:
            tokens_indices[i] = 0

    padded_sequence = pad_sequences([tokens_indices], maxlen=maxlen, truncating='post', value=0)

    prediction = model.predict(padded_sequence, verbose=0)
    sentiment = "extremely positive" if prediction[0][0] < 0.1 else "positive" if prediction[0][0] < 0.6 else "neutral" if prediction[0][0] < 0.7 else "negative" if prediction[0][0] < 0.9 else "extremely negative"
    # sentiment = "extremely positive" if prediction[0][0] > 0.9 else "positive" if prediction[0][0] > 0.6 else "neutral" if prediction[0][0] > 0.4 else "negative" if prediction[0][0] > 0.2 else "extremely negative"
    return sentiment

if __name__ == "__main__":
    print(predict(sys.argv[1]))

