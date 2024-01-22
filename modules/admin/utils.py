import os
import uuid
from Project_public.settings import PROJECT_PATH
from werkzeug.utils import secure_filename

print(PROJECT_PATH)

def check_directory(directory):
    file_path = PROJECT_PATH / f'modules/admin/static/{directory}'
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    return file_path

def update_filename(file):
    name_and_extension = list(os.path.splitext(secure_filename(file.filename)))
    name_and_extension[0] = ''.join(str(uuid.uuid4()).split('-'))
    # delete the '-'
    # change back to string
    return ''.join(name_and_extension)

def upload_file(directory_name, file):
    directory = check_directory(directory_name)
    new_file_name = update_filename(file)
    return directory / new_file_name, new_file_name

