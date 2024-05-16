import os

def read_css_file(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_dir = os.path.join(current_dir, 'styles')

    file_path = os.path.join(css_dir, file_name)

    try:
        with open(file_path, 'r') as file:
            css_content = file.read()
            return css_content
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return None
