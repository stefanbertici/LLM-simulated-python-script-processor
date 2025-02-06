import ast
import re
import subprocess

import black

def get_lines_functions_ast(content):
    tree = ast.parse(content)
    
    lines = len([line for line in content.split('\n') if line.strip()])
    functions = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
    
    return lines, functions

def get_imports_ast(content):
    tree = ast.parse(content)
    all_imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            # Handle regular imports
            all_imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            # Handle from-imports, showing both module and imported names
            module = node.module or ''  # module might be None for relative imports
            all_imports.extend(f"{module}.{alias.name}" for alias in node.names)

    return all_imports

def format_script(content):
    return black.format_str(content, mode=black.Mode())

def run_script(script_path, args=None):
    # Prepare the command - first the Python interpreter, then script path, then any arguments
    command = ['python', script_path]
    if args:
        command.extend(args)
        
    # Run the script and capture output
    # text=True makes the output return as string instead of bytes
    # capture_output=True captures both stdout and stderr
    result = subprocess.run(command, 
                            text=True,
                            capture_output=True,
                            check=True)  # This raises CalledProcessError if the script fails
    
    return result.stdout

def update_content(content, new_stats, pattern):
    if re.search(pattern, content):
        updated_content = re.sub(pattern, new_stats, content)
    else:
        if not content.endswith('\n'):
            content += '\n'
        updated_content = content + new_stats + '\n'
    
    return updated_content