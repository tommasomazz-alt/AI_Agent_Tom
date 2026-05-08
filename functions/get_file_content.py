import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    #ottieni path assoluto della working_directory
    work_dir_abspath = os.path.abspath(working_directory)

    #costruisco il path del file unendolo a quello della workdir
    target_file = os.path.normpath(os.path.join(work_dir_abspath, file_path))

    #controllo se il file è all'interno di workdir
    valid_target_file = os.path.commonpath([work_dir_abspath, target_file]) == work_dir_abspath
    
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file):
        return f'Error: file not found or is not a file "{file_path}"'
    
    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        return file_content_string
    
    except Exception as e:
        return f"Error: {e}"
    
# the code below is still WIP!!
schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)