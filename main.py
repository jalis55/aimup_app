from flask import Flask,render_template,request,redirect,url_for,flash,session, abort,jsonify

from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

from werkzeug.utils import secure_filename





app=Flask(__name__)
app.secret_key = b'_5#y2L"F92!!Q8z\n\xec]/'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aimup_app.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(50),nullable=False)
	last_name = db.Column(db.String(50),nullable=False)
	email=db.Column(db.String(50),nullable=False)
	profile_picture=db.Column(db.String(100))
	description=db.Column(db.String(100))
	password=db.Column(db.String(100),nullable=False)


class Addlisting(db.Model):
	__tablename__='addlisting'
	id=db.Column(db.Integer,primary_key=True)
	user_id=db.Column(db.Integer,nullable=False)
	title=db.Column(db.String(300),nullable=False)
	summary=db.Column(db.String(300),nullable=False)
	story=db.Column(db.String(300),nullable=False)
	additional_info=db.Column(db.String(300),nullable=False)
	expertise_area=db.Column(db.String(300),nullable=False)
	additional_specification=db.Column(db.String(300),nullable=False)
	teaching=db.Column(db.String(300),nullable=False)

#home page view
@app.route('/')
def home():
	return render_template('index.html')

#user login view
@app.route('/login')
def login():
	return render_template('login.html')

#user signup view
@app.route('/signup')
def signup():
	return render_template('signup.html')

#user signup data insertion into database
@app.route('/user-sign-up',methods=['POST'])
def user_sign_up():
	email=request.form['email']
	first_name=request.form['first_name']
	last_name=request.form['last_name']
	password=request.form['password']
	if email =='' or first_name =='' or last_name =='' or password=='':
		flash('Something went wrong. Try again!')
		return redirect(url_for('signup'))
		

	create_user=User(email=email,first_name=first_name,last_name=last_name,password=password)
	db.session.add(create_user)
	db.session.commit()
	
	flash('Your account has been created. Now log in.')
	return redirect(url_for('login'))

#user authentication process
@app.route('/user-login',methods=['POST','GET'])
def user_login():
	email=request.form['email']
	password=request.form['password']
	user = db.session.query(User).filter(User.email==email and User.password==password).first()
	if user:
		session['logged_in']=True
		session['user_id']=user.id
		flash('You are now logged in!')
		return redirect(url_for('home'))
	else:
		error='Something went wrong. Try again!'
		return render_template('login.html',error=error)

#user profile view
@app.route('/user-profile')
def user_profile():
	id=session['user_id']
	data=db.session.query(User).filter(User.id==id).first()
	print(data)
	return render_template('userprofile.html',data=data)


#user personal information update process
@app.route('/update-personal-info',methods=['POST'])
def update_personal_info():
	# image upload
	if 'img_upload' in request.form:
		user_id=request.form['user_id']
		image=request.files['profile_photo']
		filename=secure_filename(image.filename)
		image.save(os.path.join('./static/img',filename))
		user = db.session.query(User).filter(User.id==user_id).first()
		user.profile_picture=filename
		db.session.commit()
		flash('Your data has been updated!')
		return redirect(url_for('user_profile'))



	# update personal information
	if 'person_info' in request.form:
		user_id=request.form['user_id']
		description=request.form['description']
		email=request.form['email']
		first_name=request.form['first_name']
		last_name=request.form['last_name']
		user = db.session.query(User).filter(User.id==user_id).first()
		user.description = description
		user.email=email
		user.first_name=first_name
		user.last_name=last_name
		db.session.commit()
		flash('Your data has been updated!')
		return redirect(url_for('user_profile'))
	#passwoed update
	if 'password_update' in request.form:
		user_id=request.form['user_id']
		password=request.form['new_password']
		user = db.session.query(User).filter(User.id==user_id).first()
		user.password = password
		db.session.commit()
		flash('Your data has been updated!')
		return redirect(url_for('user_profile'))
	else:
		flash(' Ooops!</strong> Something went wrong. Try again!')
		return redirect(request.url)
#add listing view
@app.route('/add-listing')
def add_listing():
	user_id=session['user_id']
	return render_template('addlisting.html',user_id=user_id)

#add list data insetion in database
@app.route('/add-listing-process',methods=['POST'])
def add_listing_process():
	user_id=int(request.form['user_id'])
	title=request.form['title']
	summary=request.form['summary']
	story=request.form['story']
	additional_info=request.form['additional_info']
	expertise_area=request.form['expertise_area']
	additional_specification=request.form['additional_specification']
	teaching=request.form['teaching']
	create_addlisting=Addlisting(user_id=user_id,title=title,summary=summary,story=story,additional_info=additional_info, \
		expertise_area=expertise_area,additional_specification=additional_specification,teaching=teaching)

	db.session.add(create_addlisting)
	db.session.commit()
	flash('Your listing has been published!')
	

	return redirect(url_for('add_listing'))



#logout user
@app.route('/logout')
def logout():
	session['logged_in']=False
	session['user_id']=''
	return redirect(url_for('home'))


if __name__ == '__main__' :
	app.run(debug=True)
	db.init_app(app)