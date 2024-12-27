from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    if request.method == 'POST':
        input_text = request.form['input_text']
        if input_text:
            # Run simple_rag_agent.py with input_text and capture output
            try:
                # Pass input_text as a command-line argument to simple_rag_agent.py
                result = subprocess.run(['python', 'simple_rag_agent.py', input_text],
                                        capture_output=True, text=True, check=True)
                output = result.stdout
            except subprocess.CalledProcessError as e:
                output = f"An error occurred: {e}"
    return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)