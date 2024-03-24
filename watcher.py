import os
import random
import subprocess
import glob  # Import glob for file pattern matching
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RenameHTMLHandler(FileSystemEventHandler):
    def __init__(self, run_count, path):
        self.run_count = run_count
        self.path = path
        self.process_existing_files()

    def process_existing_files(self):
        # Scan for all existing '.html' files, not just 'pull_*.html'
        for file_path in glob.glob(os.path.join(self.path, '*.html')):
            # Rename to 'pull_*.html' if not already in that format
            if not file_path.startswith('pull_'):
                new_name = f"pull_{random.randint(1000, 9999)}.html"
                new_path = os.path.join(self.path, new_name)
                os.rename(file_path, new_path)
                print(f"Renamed {file_path} to {new_path}")
                self.process_file(new_path)
            else:
                self.process_file(file_path)

    def process_file(self, file_path):
        # This method processes each file, running main.py the specified number of times
        print(f"Processing {file_path}")
        for _ in range(self.run_count):
            subprocess.run(["python", "main.py"], check=True)
            print(f"main.py executed successfully.")

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith('.html'):
            return
        # Ensure all new .html files are renamed to 'pull_*.html'
        new_name = f"pull_{random.randint(1000, 9999)}.html"
        new_path = os.path.join(self.path, new_name)
        os.rename(event.src_path, new_path)
        print(f"Renamed {event.src_path} to {new_name}")
        self.process_file(new_path)

if __name__ == "__main__":
    run_count = int(input("How many products would you like to create per html file? "))
    print("Waiting for product HTML dumps...")
    path = 'dump'
    event_handler = RenameHTMLHandler(run_count, path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()