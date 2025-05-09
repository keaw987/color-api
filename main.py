from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO
import os
import math

app = Flask(__name__)

# 🔁 ใช้ฟังก์ชันนี้หา "ระยะห่างสี"
def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))

# ✅ ดึงหลายจุดในภาพ
@app.route("/extract-colors", methods=["POST"])
def extract_colors():
    try:
        data = request.get_json()
        base64_string = data.get("image_base64", "")

        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        # padding base64
        missing_padding = len(base64_string) % 4
        if missing_padding != 0:
            base64_string += "=" * (4 - missing_padding)

        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        width, height = image.size

        # จุดที่จะดึงสีจากภาพ
        points = [
            (0, 0),
            (width // 2, 0),
            (width // 2, height // 2),
            (width - 1, height - 1)
        ]

        colors = [image.getpixel(p) for p in points]

        return jsonify({"colors": colors})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ เปรียบเทียบกับค่าสีมาตรฐาน
@app.route("/compare-with-standard", methods=["POST"])
def compare_with_standard():
    try:
        data = request.get_json()
        base64_string = data.get("image_base64", "")
        standard_colors = data.get("standard_colors", [])

        if not standard_colors:
            return jsonify({"error": "Missing standard_colors"}), 400

        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        missing_padding = len(base64_string) % 4
        if missing_padding != 0:
            base64_string += "=" * (4 - missing_padding)

        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        width, height = image.size

        sample_points = [
            (0, 0),
            (width // 2, 0),
            (width // 2, height // 2),
            (width - 1, height - 1)
        ]

        extracted_colors = [image.getpixel(p) for p in sample_points]

        # เทียบแต่ละสีของภาพกับค่าสีมาตรฐาน
        results = []
        for c1 in extracted_colors:
            min_dist = min([color_distance(c1, c2) for c2 in standard_colors])
            results.append({"color": c1, "distance_to_closest": round(min_dist, 2)})

        return jsonify({"comparison_results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ PORT สำหรับ Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
