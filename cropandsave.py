from datetime import datetime
import os
from PIL import Image

def resize_most_recent_image():
    today_date = datetime.now().strftime("%Y-%m-%d")
    folder_path = f"focusgen/{today_date}"

    most_recent_image = None
    last_mod_time = 0
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file.lower().endswith(('.png', '.jpg', '.jpeg')):
            mod_time = os.path.getmtime(file_path)
            if mod_time > last_mod_time:
                most_recent_image = file_path
                last_mod_time = mod_time

    if most_recent_image is None:
        print("No image found.")
        return

    base_name = os.path.basename(most_recent_image)
    numerical_part = base_name.split('_')[-1].rsplit('.', 1)[0]

    resolutions = [
        ((6300, 4950), "11x14"),
        ((8400, 6000), "5x7"),
        ((7500, 6000), "4x5"),
        ((7200, 5400), "3x4"),
        ((7200, 4800), "2x3"),
    ]

    for resolution, label in resolutions:
        with Image.open(most_recent_image) as img:
            new_img = img.resize(resolution, Image.Resampling.LANCZOS)
        new_img_path = f"{folder_path}/{numerical_part}_{label}.jpg"
        new_img.save(new_img_path, "JPEG", dpi=(300, 300))
        print(f"Resized image saved as {new_img_path} with 300 DPI")

    # Delete the source image after creating all resolution images
    os.remove(most_recent_image)
    print(f"Source image {most_recent_image} deleted.")

resize_most_recent_image()
