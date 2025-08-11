from flask import Flask, request, jsonify, render_template
from utils.crypto_utils import encrypt_message, decrypt_message
from utils.ml_utils import predict_message
from utils.fuzzy_utils import apply_fuzzy_logic
from tensorflow.keras.models import load_model
import pickle 
import numpy as np
import os
app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Globals for loaded models
sklearn_model = None
keras_model = None

def load_artifacts():
    global sklearn_model, keras_model

    # Load pickle model
    pkl_path = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
    with open(pkl_path, "rb") as f:
        sklearn_model = pickle.load(f)

    # Load keras model
    keras_path = os.path.join(MODEL_DIR, "spam_classifier_model.keras")
    keras_model = load_model(keras_path)

    app.logger.info("Loaded sklearn and keras models.")

@app.before_first_request
def init():
    load_artifacts()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    plain_message = data.get('message', '')
    encrypted_msg = encrypt_message(plain_message)
    return jsonify({'encrypted_message': encrypted_msg})

@app.route('/receive', methods=['POST'])
def receive_message():
    data = request.json
    encrypted_message = data.get('encrypted_message', '')
    plain_text = decrypt_message(encrypted_message)
    ml_result, confidence = predict_message(plain_text)
    final_result = apply_fuzzy_logic(ml_result, confidence)
    return jsonify({
        'plain_message': plain_text,
        'ml_result': ml_result,
        'confidence': confidence,
        'final_decision': final_result
    })

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    msg = data.get("message", "")
    label, confidence = predict_message(msg)
    return jsonify({"label": label, "confidence": confidence})

if __name__ == "__main__":
    app.run(debug=True)
