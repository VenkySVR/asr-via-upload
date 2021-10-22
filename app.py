from flask import Flask,flash,session, request,redirect,url_for,render_template
from werkzeug.utils import secure_filename
from flask_session import Session
import os
import wave

UPLOAD_FOLDER = 'uploads/audios/'
ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def predict(file):
    return file.filename

@app.route('/',methods=["GET","POST"])
def home():
    output = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            output=predict(file)
    return render_template('index.html',output=output)

if __name__ == "__main__":
    sess = Session()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess.init_app(app)
    app.run(debug=True,port=8888)