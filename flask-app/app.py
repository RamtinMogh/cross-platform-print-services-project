from flask import Flask, request, render_template_string

import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = '/tmp/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_printers():
    result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
    return [line.split()[1] for line in result.stdout.splitlines() if line.startswith('printer')]

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    printers = get_printers()

    if request.method == 'POST':
        file = request.files['file']
        printer = request.form['printer']

        if file and printer:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)
            subprocess.run(['lp', '-d', printer, filepath])
            return redirect('/')

    return render_template_string('''
        <h1>Upload PDF to Print</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file accept="application/pdf" required><br><br>
          <label>Select printer:</label>
          <select name="printer" required>
            {% for p in printers %}
              <option value="{{p}}">{{p}}</option>
            {% endfor %}
          </select><br><br>
          <input type=submit value=Print>
        </form>
    ''', printers=printers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
