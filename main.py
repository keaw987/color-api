from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from collections import Counter
import os

app = Flask(__name__)

@app.route("/get-color", methods=["POST"])
def get_color():
    data = request.get_json()
    image_base64 = data.get("image_base64")

    if not image_base64:
        return jsonify({"error": "Missing image_base64"}), 400

    try:
        # ตัด header เช่น "data:image/png;base64," ถ้ามี
        if "," in image_base64:
            _, encoded = image_base64.split(",", 1)
        else:
            encoded = image_base64

        image_data = base64.b64decode(encoded)
        image = Image.open(BytesIO(image_data)).convert("RGB")
        pixels = list(image.getdata())
        most_common_color = Counter(pixels).most_common(1)[0][0]
        hex_color = '#%02x%02x%02x' % most_common_color
        return jsonify({"dominant_color": hex_color})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 👇 ต้องมีส่วนนี้ Render ถึงจะรัน API ได้
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
