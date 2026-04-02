import os
from config import MAX_CHAR
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
        valid_target_file = os.path.commonpath([abs_working_directory, target_file_path]) == abs_working_directory
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):    
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file_path, 'r') as file:
            content = file.read(MAX_CHAR) # limit to 10,000 characters
            if file.read(1):  # Check if there's more content beyond the limit
                content += f'[...File "{file_path}" truncated at {MAX_CHAR} characters]'
            file.close()
        
        return content
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)