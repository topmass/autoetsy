import dearpygui.dearpygui as dpg
import os
import random
import subprocess
import glob
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading

class RenameHTMLHandler(FileSystemEventHandler):
    def __init__(self, run_count, path):
        self.run_count = run_count
        self.path = path
        self.process_existing_files()

    def process_existing_files(self):
        for file_path in glob.glob(os.path.join(self.path, '*.html')):
            if not file_path.startswith('pull_'):
                new_name = f"pull_{random.randint(1000, 9999)}.html"
                new_path = os.path.join(self.path, new_name)
                os.rename(file_path, new_path)
                dpg.add_text(f"Renamed {file_path} to {new_path}", parent="file_browser")
                self.process_file(new_path)
            else:
                self.process_file(file_path)

    def process_file(self, file_path):
        dpg.add_text(f"Processing {file_path}", parent="file_browser")
        for _ in range(self.run_count):
            subprocess.run(["python", "main.py"], check=True)
            dpg.add_text(f"main.py executed successfully.", parent="file_browser")

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.html'):
            return
        new_name = f"pull_{random.randint(1000, 9999)}.html"
        new_path = os.path.join(self.path, new_name)
        os.rename(event.src_path, new_path)
        dpg.add_text(f"Renamed {event.src_path} to {new_name}", parent="file_browser")
        self.process_file(new_path)

def start_watching(path, run_count):
    event_handler = RenameHTMLHandler(run_count, path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    observer.join()

def start_processing(sender, app_data, user_data):
    path, run_count_value = user_data
    run_count = dpg.get_value(run_count_value)
    threading.Thread(target=start_watching, args=(path, run_count), daemon=True).start()

def upload_file(sender, app_data, user_data):
    file_path = app_data['file_path_name']  # Get the selected file path
    target_path = user_data  # The directory where the file should be saved
    try:
        # Ensure the target directory exists
        os.makedirs(target_path, exist_ok=True)
        # Construct the full path where the file will be saved
        save_path = os.path.join(target_path, os.path.basename(file_path))
        # Copy the file to the target directory
        with open(file_path, 'rb') as src_file:
            with open(save_path, 'wb') as dst_file:
                dst_file.write(src_file.read())
        # Update the GUI to reflect the file upload status
        dpg.add_text(f"Uploaded {os.path.basename(file_path)} successfully.", parent="file_browser")
    except Exception as e:
        # Handle potential errors during the file upload process
        dpg.add_text(f"Error uploading file: {str(e)}", parent="file_browser")

def is_image_file(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg'))

def show_image_preview(sender, app_data, user_data):
    image_path = user_data
    # Generate a unique identifier for each image preview window based on the image path
    window_id = f"preview_{os.path.basename(image_path).replace('.', '_')}"
    texture_id = f"texture_{window_id}"

    if not dpg.does_item_exist(texture_id):
        with dpg.texture_registry():
            width, height, channels, data = dpg.load_image(image_path)
            dpg.add_static_texture(width, height, data, tag=texture_id)

    if not dpg.does_item_exist(window_id):
        with dpg.window(label="Image Preview", tag=window_id):
            dpg.add_image(texture_id)
    else:
        dpg.configure_item(window_id, show=True)

def list_directory_contents(path, parent):
    try:
        for entry in sorted(os.listdir(path), key=lambda e: os.path.isdir(os.path.join(path, e)), reverse=True):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                with dpg.tree_node(label=entry, parent=parent, default_open=False):
                    list_directory_contents(full_path, parent=dpg.last_item())
            else:
                if is_image_file(entry):
                    with dpg.group(parent=parent):
                        dpg.add_text(entry)
                        dpg.add_button(label="Preview", callback=show_image_preview, user_data=full_path)
                else:
                    dpg.add_text(entry, parent=parent)
    except PermissionError:
        dpg.add_text("Permission Denied", parent=parent)

def add_file_browser_to_gui():
    with dpg.window(label="File Browser", tag="file_browser_window", width=300, height=400, pos=(300, 0)):
        list_directory_contents("export", parent="file_browser_window")

dpg.create_context()

with dpg.window(label="AutoEtsy Generator💰", tag="main_window"):
    dpg.add_file_dialog(directory_selector=False, show=False, callback=upload_file, user_data="dump", tag="file_dialog")
    dpg.add_button(label="Upload HTML files", callback=lambda: dpg.show_item("file_dialog"))
    dpg.add_text("", tag="upload_status")
    run_count = dpg.add_input_int(label="How many products per html file?", default_value=1, min_value=1)
    dpg.add_button(label="Start Processing", callback=start_processing, user_data=("dump", run_count))
    with dpg.child_window(height=300, tag="file_browser"):
        dpg.add_text("Files will be listed here.")
    add_file_browser_to_gui()

dpg.create_viewport(title='Custom Title', width=600, height=400)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context
