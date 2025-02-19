import cloudinary
import cloudinary.uploader
import os

class CloudClient:
    def __init__(self, cloud_config):
        cloudinary.config(
        cloud_name=cloud_config["cloud_name"],
        api_key=cloud_config["api_key"],
        api_secret=cloud_config["api_secret"]
)

    def uploadImage(self, screenshot):
        temp_path = "temp_image.png"
        screenshot.save(temp_path, format="PNG")

        response = cloudinary.uploader.upload(temp_path)
        os.remove(temp_path)

        return response["secure_url"]