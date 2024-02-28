import os
import random
import subprocess  # Import subprocess to run main.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RenameHTMLHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.html'):
            new_name = f"pull_{random.randint(1000, 9999)}.html"
            os.rename(event.src_path, os.path.join('dump', new_name))
            print(f"Renamed {event.src_path} to {new_name}")
            # Run main.py after renaming the .html file
            subprocess.run(["python", "extract.py"], check=True)
            print("main.py executed successfully.")

if __name__ == "__main__":
    path = 'dump'
    event_handler = RenameHTMLHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()