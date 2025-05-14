from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return 'API is running!'

@app.route('/get-color', methods=['POST'])
def get_color():
    # ประมวลผล base64 → image
    return jsonify({"color": [255, 255, 255]})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
