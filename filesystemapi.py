from werkzeug.utils import secure_filename
import random
import string
import os
from datetime import datetime

class FileInfo:
    def __init__(self, filename, size, date):
        self.filename = filename
        self.size = size
        self.date = date

    def __repr__(self):
        return f"FileInfo(filename={self.filename}, size={self.size}, date={self.date})"


class FilesystemApi:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder


    def ReadBinary(self, filename):
        #file_path = filename
        #try:
        #    with open(file_path, "rb") as f:
        #
        #except FileNotFoundError:
        #    print(f"File not found: {file_path}")
        #    return False
        #except requests.exceptions.RequestException as e:
        #    print(f"An error occurred: {e}")
        #    return False
        filepath = os.path.join(self.upload_folder, filename)
        with open(filepath, "rb") as f:
            data = f.read()
        return data


    def WriteBinary(self, filename, data):
        rand = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
        fname = rand + "." + secure_filename(filename)
        file_path = os.path.join(self.upload_folder, fname)
        with open(file_path, "wb") as f:
            f.write(data)
        return fname


    def ListResult(self):
        files = []
        for entry in os.scandir(self.upload_folder):
            if entry.is_file():
                if not entry.name.endswith('.json'):
                    continue
                file_info = FileInfo(
                    filename=entry.name,
                    size=int(entry.stat().st_size / 1024),
                    date=datetime.fromtimestamp(entry.stat().st_mtime).strftime('%Y.%m.%d')
                )
                files.append(file_info)
        return files


    def WriteResult(self, filename, data):
        file_path = os.path.join(self.upload_folder, filename + ".json")
        with open(file_path, "w") as f:
            f.write(data)
        return True
    

    def ReadResult(self, filename):
        file_path = os.path.join(self.upload_folder, filename)
        with open(file_path, "r") as f:
            data = f.read()
        return data