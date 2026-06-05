def extract_text_from_txt(file_path: str) -> str:

    # open() is Python's built-in file reader
    # 'r' means read mode
    # encoding='utf-8' handles special characters properly
    with open(file_path, 'r', encoding='utf-8') as file:
        
        # read() loads the entire file content at once
        content = file.read()
    
    # 'with' block automatically closes the file here
    # no need to call file.close() manually
    
    return content