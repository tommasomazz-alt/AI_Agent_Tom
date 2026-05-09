from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_files_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file


available_functions = types.Tool(
    function_declarations=[schema_get_files_info, 
                           schema_get_files_content, 
                           schema_run_python_file,
                           schema_write_file],
)

# funzione per la task astratta di chiamare una delle nostre quattro funzioni e restituirne i risultati
def call_function(function_call, verbose=False):

    # volendo la funzione chiamata può essere None quindi la associo a una variabile e se è None restituisco errore
    function_name = function_call.name or ""

    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    if function_name not in function_map:

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    # faccio una copia shallow degli arguments poichè la working_directory la sovrascriveremo
    args = dict(function_call.args) if function_call.args else {}

    args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )