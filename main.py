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
