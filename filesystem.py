from werkzeug.utils import secure_filename
import random
import string
import os


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
        fname = secure_filename(filename)
        rand = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
        file_path = os.path.join(self.upload_folder, rand + "." + fname)
        with open(file_path, "wb") as f:
            f.write(data)
        return fname


    def ListResult(self):
        files = [f for f in os.listdir(self.upload_folder) if f.endswith('.json')]
        return files


    def WriteResult(self, filename, data):
        file_path = os.path.join(self.upload_folder, filename + ".json")
        with open(file_path, "w") as f:
            f.write(data)
        return True
    

    def ReadResult(self, filename):
        file_path = os.path.join(self.upload_folder, filename + ".json")
        with open(file_path, "r") as f:
            data = f.read()
        return data