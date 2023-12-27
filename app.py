from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_code = request.form['pseudocode']

        # Write the input code to the .tiny file
        with open("input.tiny", 'w') as file:
            file.write(input_code)

        # Ensure the Java command is correct for your operating system
        # On Windows, it's typically just 'java', but it could be a full path like 'C:\\Path\\to\\Java\\bin\\java.exe'
        java_command = "C:\SDKs\Java\\bin\java.exe"

        # The classpath should point to the directory containing compiled .class files
        java_class_path = 'Java'  # Adjust as necessary
        java_class = 'A5'  # running main class

        try:
            result = subprocess.run(
                [java_command, '-cp', java_class_path, java_class, input_code],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            if result.stderr:
                output = result.stderr
            else:
                output = result.stdout.strip().split()[-1]

            if output == 'false':
                return jsonify("Invalid TINY syntax")

            with open("input.tiny", 'r') as file:
                result = subprocess.run(
                    [java_command, '-cp', java_class_path, "A4User", 'input.tiny'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            codefile = open("code.java","r")
            code = codefile.read()
            codefile.close()
            return jsonify(code)

        except FileNotFoundError as e:
            error_message = f"An error occurred: {e}. Make sure Java is installed and the path to the Java executable is correct."
            print(error_message)
            return jsonify(error_message), 500

        except Exception as e:
            # Generic exception catch to ensure any other issues are caught and logged
            error_message = f"An unexpected error occurred: {e}"
            print(error_message)
            return jsonify(error_message), 500

    # If it's a GET request, just render the form
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
