import os
from google.genai import types

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
    

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file in a specified file_path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path","content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to be modified, relative to the working directory"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written or overwritten to the file"
            )
        },
    ),
)

