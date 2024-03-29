import os
import random
import subprocess
import glob
import streamlit as st
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
                st.write(f"Renamed {file_path} to {new_path}")
                self.process_file(new_path)
            else:
                self.process_file(file_path)

    def process_file(self, file_path):
        st.write(f"Processing {file_path}")
        for _ in range(self.run_count):
            subprocess.run(["python", "main.py"], check=True)
            st.write(f"main.py executed successfully.")

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.html'):
            return
        new_name = f"pull_{random.randint(1000, 9999)}.html"
        new_path = os.path.join(self.path, new_name)
        os.rename(event.src_path, new_path)
        st.write(f"Renamed {event.src_path} to {new_name}")
        self.process_file(new_path)

def save_uploaded_file(uploaded_file, path):
    if uploaded_file is not None:
        with open(os.path.join(path, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        return True
    return False

if __name__ == "__main__":
    st.title("HTML File Processor")
    uploaded_file = st.file_uploader("Upload HTML files", type="html")
    run_count = st.number_input("How many products would you like to create per html file?", min_value=1, value=1, step=1)
    path = 'dump'
    if not os.path.exists(path):
        os.makedirs(path)
    if uploaded_file is not None and save_uploaded_file(uploaded_file, path):
        st.success(f"Uploaded {uploaded_file.name} successfully.")
    event_handler = RenameHTMLHandler(run_count, path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    st.write("Waiting for product HTML dumps...")
    observer.stop()
    observer.join()
