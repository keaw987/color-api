from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from collections import Counter

app = Flask(__name__)

@app.route("/get-color", methods=["POST"])
def get_color():
    data = request.get_json()
    image_base64 = data.get("image_base64")

    if not image_base64:
        return jsonify({"error": "Missing image_base64"}), 400

    try:
        # ✅ ดึงเฉพาะส่วน base64 (ตัด data:image/... ออก ถ้ามี)
        if "," in image_base64:
            header, encoded = image_base64.split(",", 1)
        else:
            encoded = image_base64

        # ✅ ถอดรหัส base64 เป็น binary image
        image_data = base64.b64decode(encoded)

        # ✅ โหลดภาพจาก binary แล้วแปลงเป็น RGB
        image = Image.open(BytesIO(image_data)).convert("RGB")

        # ✅ หาค่าสีที่พบมากที่สุด
        pixels = list(image.getdata())
        most_common_color = Counter(pixels).most_common(1)[0][0]
        hex_color = '#%02x%02x%02x' % most_common_color

        return jsonify({"dominant_color": hex_color})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
