@app.route("/get-color", methods=["POST"])
def get_color():
    data = request.get_json()
    image_base64 = data.get("image_base64")

    if not image_base64:
        return jsonify({"error": "Missing image_base64"}), 400

    try:
        # ✅ กรอง base64 ให้ถูกต้อง
        if "," in image_base64:
            header, encoded = image_base64.split(",", 1)
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
