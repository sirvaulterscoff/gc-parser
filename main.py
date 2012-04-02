from flask import Flask, render_template, session, request, redirect, url_for, flash
from werkzeug import secure_filename
import os
from parser import parse

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = '\r\xad!\x10r\xf3$\x97\xc6\x9b\x04\xff\xaayp\x15\xbd\xca\x955U(k\xe0'

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/submit_log', methods = ['POST'])
def submit_log():
    _file = request.files['file1']
    data = None
    if _file:
        filename = secure_filename(_file.filename)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        _file.save(filename)
        data = parse('SUN', filename)
    print data
    if data:
        return render_template('result.html', data=data)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    print 'Running in Debug:%s mode' % app.config['DEBUG']
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])
