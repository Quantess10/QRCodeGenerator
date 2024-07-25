import base64

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string

# Przykład użycia
encoded_image = encode_image_to_base64('main_image.jpg')
print(encoded_image)
