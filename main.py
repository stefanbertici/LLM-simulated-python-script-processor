import subprocess
from utils.analyze_utils import format_script, get_lines_functions_ast
from utils.analyze_utils import get_imports_ast
from utils.analyze_utils import run_script
import argparse
import datetime
import re

def main():
    parser = argparse.ArgumentParser("python code reviewer")
    parser.add_argument("file_name", help="name of the python script to be reviewed")
    parser.add_argument("--document", action="store_true", help="count the number of functions and lines in the script, then append this information as a comment at the end of the file")
    parser.add_argument("--analyze", action="store_true", help="identify and list the imported modules in the script, appending them as a comment")
    parser.add_argument("--execute", action="store_true", help="run the script and optionally capture its output")
    parser.add_argument("--format", action="store_true", help="use an external library to automatically format the script")
    args = parser.parse_args()

    try:
        if args.file_name:
            print(f'~~~ analyzing file named "{args.file_name}"')

        if args.document:
            with open(args.file_name, 'r') as file:
                content = file.read()
                
                lines, functions = get_lines_functions_ast(content)
                current_dateTime = datetime.datetime.now()
                new_stats = f"# lines of code = {lines}, functions = {functions} @{current_dateTime}"
                print(new_stats)
        
                pattern = r"# lines of code = \d+, functions = \d+ @\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+"
    
                if re.search(pattern, content):
                    updated_content = re.sub(pattern, new_stats, content)
                else:
                    if not content.endswith('\n'):
                        content += '\n'
                    updated_content = content + new_stats + '\n'
    
            with open(args.file_name, 'w') as file:
                file.write(updated_content)
        
        if args.analyze:
            with open(args.file_name, 'r') as file:
                content = file.read()

                imports = ", ".join(get_imports_ast(content))
                current_dateTime = datetime.datetime.now()
                new_stats = f"# imports = {imports} @{current_dateTime}"
                print(new_stats)
        
                pattern = r"# imports = [a-zA-Z, ]* @\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+"
    
                if re.search(pattern, content):
                    updated_content = re.sub(pattern, new_stats, content)
                else:
                    if not content.endswith('\n'):
                        content += '\n'
                    updated_content = content + new_stats + '\n'
    
            with open(args.file_name, 'w') as file:
                file.write(updated_content)

        if args.format:
            with open(args.file_name, 'r') as file:
                content = file.read()
                print("formatting script...")
                formatted_content = format_script(content)

                with open(args.file_name, 'w') as file:
                    file.write(formatted_content)

        if args.execute:
                print("running script...")
                standard = run_script(args.file_name, [])
                print(f"standard output: {standard}")

    except FileNotFoundError:
        print(f"Could not find the script at {args.file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")
    except subprocess.CalledProcessError as e:
        print(f"The script failed with return code {e.returncode}")
        print(f"Error output: {e.stderr}")
        
if __name__ == '__main__':
    main()