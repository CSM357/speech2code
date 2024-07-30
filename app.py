import os
import subprocess
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def create_python_file(file_name, vs_code_path):
    file_path = os.path.join(os.getcwd(), file_name + '.py')

    try:
        with open(file_path, 'w') as file:
            file.write('# This is a new Python file\n')

        subprocess.Popen([vs_code_path, file_path])

        return f"Python file '{file_name}.py' created at '{file_path}'."
    except Exception as e:
        return f"Error: {e}"


def create_hello_world_program(file_name, vs_code_path):
    file_path = os.path.join(os.getcwd(), file_name + '.py')

    try:
        with open(file_path, 'w') as file:
            file.write('# Python program to print "Hello, world!"\n\n')
            file.write('print("Hello, world!")\n\n')

        subprocess.Popen([vs_code_path, file_path])

        return f"Python program '{file_name}.py' created with 'Hello, world!' at '{file_path}'."
    except Exception as e:
        return f"Error: {e}"


def create_variable(file_name, vs_code_path, var_name, var_value):
    file_path = os.path.join(os.getcwd(), file_name + '.py')

    try:
        with open(file_path, 'w') as file:
            file.write(f'# Python program to define variable {var_name}\n\n')
            file.write(f'{var_name} = {var_value}\n')

        subprocess.Popen([vs_code_path, file_path])

        return f"Python program '{file_name}.py' created with variable '{var_name}' assigned to '{var_value}' at '{file_path}'."
    except Exception as e:
        return f"Error: {e}"


def run_python_file_in_vscode(file_name, vs_code_path):
    file_path = os.path.join(os.getcwd(), file_name + '.py')

    try:

        subprocess.Popen([vs_code_path, '--new-terminal', '--wait', '--command', f'python3 {file_path}'])
        return f"Python file '{file_name}.py' opened and executed with Python 3 in Visual Studio Code."
    except Exception as e:
        return f"Error: {e}"


def process_command(command):
    command = command.lower().strip()

    if 'open vs code' in command:
        vs_code_path = r'C:\Users\chandra shekhar mish\AppData\Local\Programs\Microsoft VS Code\Code.exe'
        subprocess.Popen([vs_code_path])
        return "Visual Studio Code opened."

    elif 'create python file' in command:
        file_name = 'p1'
        vs_code_path = r'C:\Users\chandra shekhar mish\AppData\Local\Programs\Microsoft VS Code\Code.exe'
        result = create_python_file(file_name, vs_code_path)
        return result

    elif 'write hello world' in command:
        file_name = 'p1'
        vs_code_path = r'C:\Users\chandra shekhar mish\AppData\Local\Programs\Microsoft VS Code\Code.exe'
        result = create_hello_world_program(file_name, vs_code_path)
        return result

    elif command.startswith('variable'):

        try:
            _, var_name, var_value = command.split()
            var_value = eval(var_value)
            file_name = 'p1'
            vs_code_path = r'C:\Users\chandra shekhar mish\AppData\Local\Programs\Microsoft VS Code\Code.exe'
            result = create_variable(file_name, vs_code_path, var_name, var_value)
            return result
        except Exception as e:
            return f"Error processing command: {e}"

    elif 'run' in command:
        file_name = 'p1'
        vs_code_path = r'C:\Users\chandra shekhar mish\AppData\Local\Programs\Microsoft VS Code\Code.exe'
        result = run_python_file_in_vscode(file_name, vs_code_path)
        return result

    else:
        return "No valid command recognized. Please try again with supported operations."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        if 'command' in data:
            speech_input = data['command']

            python_code = process_command(speech_input)

            if python_code is not None:
                return jsonify({'output': python_code}), 200
            else:
                return jsonify({'error': 'Invalid command.'}), 400
        else:
            return jsonify({'error': 'Invalid request. Missing "command" parameter.'}), 400
    except Exception as e:
        print(f"Error during translation: {e}")
        return jsonify({'error': 'Unable to process the command. Please try again later.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
