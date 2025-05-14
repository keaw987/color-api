from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO
import base64
import os

app = Flask(__name__)

def decode_image(base64_string):
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
        raise ValueError(f"Base64 decode/open failed: {e}")

@app.route("/get-color", methods=["POST"])
def get_color():
    try:
        data = request.get_json()
        image = decode_image(data.get("image_base64", ""))
        color = image.getpixel((0, 0))
        return jsonify({"color": color})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
