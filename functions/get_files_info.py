import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    #ottieni path assoluto della working_directory
    work_dir_abspath = os.path.abspath(working_directory)

    #costruisce il path della directory target unendolo a quello della workdir
    target_dir = os.path.normpath(os.path.join(work_dir_abspath,directory))

    #controlla se target_dir è all'interno di working_dir
    valid_target_dir = os.path.commonpath([work_dir_abspath,target_dir]) == work_dir_abspath
    
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        target_dir_content = []
        for item in os.listdir(target_dir):
            name = item
            size = os.path.getsize(os.path.join(target_dir,item))
            is_dir = os.path.isdir(os.path.join(target_dir,item))
            line = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            target_dir_content.append(line)
        final_string = "\n".join(target_dir_content)

        return final_string
    
    except Exception as e:
        return f"Error: {e}"

# see here for an explanation: https://www.boot.dev/lessons/65d175bf-d169-4234-85d1-e57e0ef93373
# basically the below is a standard format to describa a function for LLM callers
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
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

