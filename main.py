def decode_image(base64_string):
    if not base64_string:
        raise ValueError("Empty base64 string.")

    # ตัด prefix "data:image/jpeg;base64," ออก
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]

    # ล้าง character ที่ไม่ใช่ base64
    base64_string = base64_string.replace("\n", "").replace("\r", "").replace(" ", "")
    base64_string += "=" * ((4 - len(base64_string) % 4) % 4)  # ปรับ padding

    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data))
        image = image.convert("RGB")
        return image
    except Exception as e:
        raise ValueError(f"Base64 decode/open failed: {e}")
