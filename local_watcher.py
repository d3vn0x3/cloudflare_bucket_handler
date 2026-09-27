import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BucketSyncHandler(FileSystemEventHandler):
    def __init__(self, r2_manager, bucket_name, local_dir):
        super().__init__()
        self.r2 = r2_manager
        self.bucket_name = bucket_name
        self.local_dir = local_dir

    def on_created(self, event):
        # Ignore directory creation events
        if event.is_directory:
            return

        filepath = event.src_path
        filename = os.path.basename(filepath)

        # Ignore temporary or hidden system files (e.g., .tmp, ~$ files)
        if filename.startswith(".") or filename.startswith("~$"):
            return

        # Give the system time to finish writing the file
        time.sleep(1)

        try:
            print(f"[Watcher] New file detected: {filename}. Uploading to {self.bucket_name}...")
            self.r2.upload_file(filepath, self.bucket_name, filename)
            print(f"[Watcher] Successfully synced {filename} to {self.bucket_name}.")
        except Exception as e:
            print(f"[Watcher] Failed to upload {filename}: {e}")

class LocalWatcher:
    def __init__(self, r2_manager, public_dir, private_dir):
        self.r2 = r2_manager
        self.public_dir = public_dir
        self.private_dir = private_dir
        self.observer = Observer()

    def start(self):
        # Watcher for local Public folder
        public_handler = BucketSyncHandler(
            self.r2, self.r2.bucket_public, self.public_dir
        )
        self.observer.schedule(public_handler, self.public_dir, recursive=False)

        # Watcher for local Private folder
        private_handler = BucketSyncHandler(
            self.r2, self.r2.bucket_private, self.private_dir
        )
        self.observer.schedule(private_handler, self.private_dir, recursive=False)

        self.observer.start()
        print("[Watcher] Background folder watchers started successfully.")

    def stop(self):
        self.observer.stop()
        self.observer.join()
        print("[Watcher] Folder watchers stopped.")