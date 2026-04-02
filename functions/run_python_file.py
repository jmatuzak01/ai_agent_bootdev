import os
import shlex
import subprocess
import sys
from google.genai import types
def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_target_file = os.path.commonpath([abs_working_directory, target_file_path]) == abs_working_directory
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        #subprocess
        command =[sys.executable, target_file_path]
        if args:
            command.extend(shlex.split(args))
        command_result = subprocess.run(command, text=True, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_string = ''
        if command_result.returncode != 0:
            output_string += f"Process exited with code {command_result.returncode}\n"
        if command_result.stdout or command_result.stderr:
            output_string += f"STDOUT:{command_result.stdout}\n"
            output_string += f"STDERR:{command_result.stderr}\n"
        else:
            output_string += "No output produced\n"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of command-line arguments to pass to the Python file",
            ),
        },
        required=["file_path"],
    ),
)