import zipfile

def compress_to_zip(file_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(file_path, arcname=file_path.split("/")[-1])