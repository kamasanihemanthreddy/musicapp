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
		search = request.form.get('search',None)
		album = request.form.get('album',None)
		if album:
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
				db.session.close()
				return redirect(url_for('home'))
			else:
				flash("file is not an mp3 format")
				# return render_template('index.html',ismp3=False)
		if search:
			album = MusicLibirary.query.filter_by(album=search)
			title = MusicLibirary.query.filter_by(title=search)
			artist = MusicLibirary.query.filter_by(artist=search)
			if album.count() > 0:
				return render_template('index.html', music_records=album)
			elif artist.count() > 0:
				return render_template('index.html', music_records=artist)
			elif title.count() > 0:
				return render_template('index.html', music_records=title)
			else:
				flash("No search result Found ")
	music_records = MusicLibirary.query.all()
	return render_template('index.html', music_records=music_records)

@app.route('/add',methods=['GET'])
def addsong():
	return render_template('uploadsongs.html')

	

@app.route('/music/delete/',methods=['POST','GET'])
def delete_entry():
	delete_id = request.form['id']
	ms_obj = MusicLibirary.query.filter_by(id=delete_id)
	if ms_obj.count() > 0:
		os.remove(os.path.join(app.config['UPLOAD_FOLDER'], ms_obj.first().filname))
		ms_obj.delete()
		db.session.commit()
		db.session.close()
	else:
		return jsonify(error="No object to delete ")
	return jsonify(data="deleted success fully")

@app.route('/search',methods=['GET','POST'])
def search():
	search = request.form['search']
	album = MusicLibirary.query.filter_by(album=search)
	title = MusicLibirary.query.filter_by(title=search)
	artist = MusicLibirary.query.filter_by(artist=search)
	if album.count() > 0:
		return render_template('index.html', music_records=album)
	elif artist.count() > 0:
		return render_template('index.html', music_records=artist)
	elif title.count() > 0:
		return render_template('index.html', music_records=title)
	else:
		flash("No search result Found ")
		music_records = MusicLibirary.query.all()
		return render_template('index.html', music_records=title)
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