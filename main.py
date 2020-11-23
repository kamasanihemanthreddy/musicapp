from flask import *
import sqlite3 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os 
from datetime import datetime, date  
import uuid

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "musicdatabase.db"))

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SECRET_KEY'] = 'this is a secretkey for music app'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)


FILE_TYPES = set(['mp3'])

@app.route('/',methods=['POST','GET'])
def home():
	if request.form:
		file = request.files['file']
		submit_name = request.files['file'].filename
		file.filename =  str(uuid.uuid1())+str(date.today())+'.mp3'
		# filename = secure_filename(file.filename)
		filename = file.filename
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		if '.' in submit_name and submit_name.rsplit('.', 1)[1] in FILE_TYPES:
			# if '.mp3' not in  request.files['file'].filename:
			music = MusicLibirary(title=request.form.get("title"),
					album=request.form.get("album"),
					artist=request.form.get("artist"),
					filname=file.filename,
					file_path=file_path)
			db.session.add(music)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			db.session.commit()
		else:
			flash("file is not and mp3 format")
			# return render_template('index.html',ismp3=False)
	music_records = MusicLibirary.query.all()
	return render_template('index.html', music_records=music_records)

@app.route('/music/delete/',methods=['POST','GET'])
def delete_entry():
	delete_id = request.form['id']
	ms_obj = MusicLibirary.query.filter_by(id=delete_id)
	if bool(ms_obj):
		ms_obj.delete()
		db.session.commit()
	else:
		return jsonify(error="No object to delete ")
	return jsonify(data="deleted success fully")

"""Model fields """
class MusicLibirary(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(100), unique=False, nullable=False)
	album = db.Column(db.String(100), unique=False, nullable=False)
	artist = db.Column(db.String(100), unique=False, nullable=False)
	filname = db.Column(db.String(255), unique=False, nullable=False)
	file_path = db.Column(db.String(300), unique=False, nullable=False)
	# file = db.Column(db.LargeBinary)

	def __repr__(self):
		return "<Title: {}>".format(self.title)

if __name__ == "__main__":
	app.run(debug=True)