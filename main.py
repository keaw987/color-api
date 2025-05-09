from flask import Flask, request, jsonify
import base64
from PIL import Image
from io import BytesIO
import os

app = Flask(__name__)

@app.route("/get-color", methods=["POST"])
def get_color():
    try:
        data = request.get_json()
        base64_string = data.get("image_base64", "")

        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        # ทำ padding ให้ถูกต้อง
        missing_padding = len(base64_string) % 4
        if missing_padding != 0:
            base64_string += "=" * (4 - missing_padding)

        # แปลง base64 เป็นภาพ
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))

        # เอาสี pixel แรก
        pixel = image.getpixel((0, 0))

        return jsonify({"color": pixel})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ แก้ให้ Flask ใช้ PORT จาก Render ได้
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
