import os

def write_file(working_directory, file_path, content):
    work_dir_abspath = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(work_dir_abspath, file_path))

    valid_target_file = os.path.commonpath([work_dir_abspath, target_file]) == work_dir_abspath

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    # mi assicuro che le parent directories di file_path esistano o le creo

    try:
        os.makedirs(os.path.dirname(target_file), mode=0o777, exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f'Error: {e}'
    


