import zipfile
import os

def extract_py_files(zip_file_path, output_folder):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.py'):
                # Extract the file while preserving the folder structure
                zip_ref.extract(file_info, output_folder)

if __name__ == '__main__':
    zip_file_path = 'path/to/your/zip/file.zip'
    output_folder = 'path/to/your/output/folder'
    extract_py_files(zip_file_path, output_folder)
