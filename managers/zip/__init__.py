import zipfile
import os


class ZipHandler:
    def __init__(self, zip_filename):
        self.zip_filename = zip_filename

    def create_zip(self):
        with zipfile.ZipFile(self.zip_filename, "w") as zip_file:
            pass

    def add_file(self, file_path):
        if os.path.exists(file_path):
            with zipfile.ZipFile(self.zip_filename, "a") as zip_file:
                zip_file.write(file_path, os.path.basename(file_path))
        else:
            print(f"File '{file_path}' does not exist.")

    def get_zip_link(self):
        return f"Path to the zip file: {self.zip_filename}"

    def predict_zip_size(self):
        total_size = 0
        for root, _, files in os.walk("."):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
        return total_size

    def get_zip_details(self):
        zip_info = []
        with zipfile.ZipFile(self.zip_filename, "r") as zip_file:
            for info in zip_file.infolist():
                zip_info.append(
                    {
                        "filename": info.filename,
                        "file_size": info.file_size,
                        "compress_size": info.compress_size,
                    }
                )
        return zip_info