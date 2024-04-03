import gradio as gr
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
                self.process_file(new_path)
            else:
                self.process_file(file_path)

    def process_file(self, file_path):
        for _ in range(self.run_count):
            subprocess.run(["python", "main.py"], check=True)

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.html'):
            return
        new_name = f"pull_{random.randint(1000, 9999)}.html"
        new_path = os.path.join(self.path, new_name)
        os.rename(event.src_path, new_path)
        self.process_file(new_path)

def start_watching(path, run_count):
    event_handler = RenameHTMLHandler(run_count, path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

def start_processing(run_count):
    path = "dump"
    # Convert run_count to integer
    run_count = int(run_count)
    threading.Thread(target=start_watching, args=(path, run_count), daemon=True).start()
    return "Processing started."

def upload_file(file_path):
    target_path = "dump"
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if file_path is not None:
        original_filename = os.path.basename(file_path)
        save_path = os.path.join(target_path, original_filename)
        os.rename(file_path, save_path)
        return f"Uploaded {original_filename} successfully."
    return "No file uploaded."

def create_gradio_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## AutoEtsy Generator💰")
        with gr.Row():
            file_upload = gr.File(label="Upload HTML files", type="filepath")
            run_count = gr.Number(label="How many products per html file?", value=1, step=1)
            start_btn = gr.Button("Start Processing")
        output_text = gr.Textbox(label="Console Output")

        file_upload.change(fn=upload_file, inputs=file_upload, outputs=output_text)
        start_btn.click(fn=lambda count: start_processing(count), inputs=run_count, outputs=output_text)

    demo.launch()

if __name__ == "__main__":
    create_gradio_interface()