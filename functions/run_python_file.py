import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    work_dir_abspath = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(work_dir_abspath, file_path))

    valid_target_file = os.path.commonpath([work_dir_abspath, target_file]) == work_dir_abspath

    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not target_file.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    # creo il comando per il sottoprocesso
    command = ["python", target_file]

    # se sono stati passati argomenti extra li aggiungo al comando
    if args != None:
        command.extend(args)

    # chiamo il sottoprocesso
    try:
        result = subprocess.run(
            command,
            cwd=work_dir_abspath,
            capture_output=True,
            text=True,
            timeout=30,
            )
        
        output_string = ""

        if result.returncode != 0:
            output_string += f"\nProcess exited with code {result.returncode}"

        if result.stdout == "" and result.stderr == "":
            output_string += f"\nNo output produced"

        else:
            if result.stdout != "":
                output_string += f'\nSTDOUT: {result.stdout}'
            if result.stderr != "":
                output_string += f'\nSTDERR: {result.stderr}'

        return output_string
    
    except Exception as e:
        return f'Error: {e}'
        