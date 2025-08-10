from flask import Flask, request, jsonify, render_template
from utils.crypto_utils import encrypt_message, decrypt_message
from utils.ml_utils import predict_message
from utils.fuzzy_utils import apply_fuzzy_logic

app = Flask(__name__)

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
