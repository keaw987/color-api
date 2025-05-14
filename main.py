from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64
import os

app = Flask(__name__)

# ================== decode_image (ที่คุณมีแล้ว) ==================
def decode_image(base64_string):
    if not base64_string:
        raise ValueError("Empty base64 string.")

    if "," in base64_string:
        base64_string = base64_string.split(",")[1]

    base64_string = base64_string.replace("\n", "").replace("\r", "").replace(" ", "")
    base64_string += "=" * ((4 - len(base64_string) % 4) % 4)

    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        image = image.convert("RGB")
        return image
    except Exception as e:
        raise ValueError("Base64 decode/open failed: {}".format(e))

# ================== Endpoint 1: ตรวจสีจากตำแหน่งเดียว ==================
@app.route("/get-color", methods=["POST"])
def get_color():
    try:
        data = request.get_json()
        image = decode_image(data.get("image_base64", ""))
        pixel = image.getpixel((0, 0))  # เปลี่ยนตำแหน่งได้
        return jsonify({"r": pixel[0], "g": pixel[1], "b": pixel[2], "actual": "#{:02X}{:02X}{:02X}".format(*pixel)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================== Endpoint 2: ตรวจหลายจุด ==================
@app.route("/extract-colors", methods=["POST"])
def extract_colors():
    try:
        data = request.get_json()
        image = decode_image(data.get("image_base64", ""))
        positions = data.get("positions", [])
        colors = [image.getpixel(tuple(pos)) for pos in positions]
        return jsonify({"colors": colors})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================== Endpoint 3: เปรียบเทียบกับมาตรฐาน ==================
@app.route("/compare-with-standard", methods=["POST"])
def compare_with_standard():
    try:
        data = request.get_json()
        image = decode_image(data.get("image_base64", ""))
        positions = data.get("positions", [])
        standard_colors = data.get("standard_colors", [])

        results = []
        for pos, std_color in zip(positions, standard_colors):
            actual = image.getpixel(tuple(pos))
            match = actual == tuple(std_color)
            results.append({
                "position": pos,
                "actual": actual,
                "expected": std_color,
                "match": match
            })

        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================== START SERVER ==================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
