import tensorflow as tf
import pickle
import numpy as np
import os

# Load model and tokenizer ONCE when module is imported
model = tf.keras.models.load_model(os.path.join('model', 'spam_model.h5'))
with open(os.path.join('model', 'tokenizer.pickle'), 'rb') as handle:
    tokenizer = pickle.load(handle)
maxlen = 50   # Set to the maxlen used during training

def preprocess(text):
    seq = tokenizer.texts_to_sequences([text])
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    padded = pad_sequences(seq, maxlen=maxlen)
    return padded

def predict_message(msg):
    x = preprocess(msg)
    pred = model.predict(x, verbose=0)[0][0]    # For binary classification
    label = 'spam' if pred > 0.5 else 'ham'
    confidence = float(pred) if pred > 0.5 else 1 - float(pred)
    return label, confidence
