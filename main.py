from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return 'API is running ✅'

@app.route('/get_color', methods=['POST'])
def get_color():
    try:
        data = request.get_json()
        base64_str = data.get('image_base64')

        # แปลง base64 เป็นรูป
        image_data = base64.b64decode(base64_str)
        image = Image.open(BytesIO(image_data))

        # หาค่า RGB ตรงกลางภาพ
        w, h = image.size
        pixel = image.getpixel((w // 2, h // 2))

        return jsonify({
            "R": pixel[0],
            "G": pixel[1],
            "B": pixel[2]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
