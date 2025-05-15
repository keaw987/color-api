from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64
import os

app = Flask(__name__)

def decode_image(base64_string):
    try:
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]  # ตัด prefix ออก

        # ล้างอักขระพิเศษ และเติม padding
        base64_string = base64_string.replace("\n", "").replace("\r", "").replace(" ", "")
        base64_string += "=" * ((4 - len(base64_string) % 4) % 4)

        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        image = image.convert("RGB")  # ให้แน่ใจว่ารูปอยู่ใน RGB mode
        return image
    except Exception as e:
        raise ValueError(f"Base64 decode/open failed: {e}")

@app.route("/")
def root():
    return "API is running!"

@app.route("/get-color", methods=["POST"])
def get_color():
    try:
        data = request.get_json()
        image = decode_image(data.get("image_base64", ""))
        pixel = image.getpixel((0, 0))
        return jsonify({"color": pixel})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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

# ✅ สำหรับใช้งานบน Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
