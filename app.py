# import necessary libraries
import os
import numpy as np
import pandas as pd
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    url_for)

from config import config
from werkzeug.utils import secure_filename
from flask import send_from_directory
#sys.path.insert(0, './db')
from db.analysis import fx_analysis, fx_result

#from flask.ext.cors import CORS
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#config_name = os.getenv("FLASK_ENV", "default")
config_name = "development"
app.config.from_object(config[config_name])

#CORS(app, headers=['Content-Type'])


######################################################

@app.route('/submit_form', methods=['GET', 'POST'])
def model_upload():
    if request.method == 'POST':
        time_series = request.form.get('time-series')
        dimension = request.form.get('dimension')
        label = request.form.get('label')
        fact = request.form.get('fact')
        model = request.form.get('model')

        # to debug
        form = dict(request.form)
        for k, v in form.items():
            print(str(k) + ":" + str(v))

        # call model, do magic and return to template
        return ('Got: time_series={}, dimension={}, label={}, fact={}, model={}'
                .format(time_series, dimension, label, fact, model))

    else:
        return "Nothing to see here."

######################################################

# create route that renders index.html template
@app.route("/")
def home():
    """Return the dashboard homepage"""
    return render_template("index.html")


#########################################

@app.route('/upload')
def upload_complete():

    """Saves imported folder to server"""

    UPLOAD_FOLDER = 'db/data'
    ALLOWED_EXTENSIONS = set(['csv'])

    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return ''

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#########################################
@app.route('/submit/<v_uk_id>')
def submit_complete(v_uk_id):
    """
	a. JSON file of the column type allocation saved to ./uk_id folder
	b. python function has been called like  (uk_id)
	c. Calls fx_result(uk_id) that return 'Processing' or 'Ready'
	d. if processing then show processing else show result in graph section.
	   Template (submit_complete.html) can use jpeg file saved for 6 graphs and json files for any data.
    """


    return render_template("result.html")

#################################################
if __name__ == "__main__":
    app.run(debug=True)