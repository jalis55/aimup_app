from flask import Flask,render_template,request,redirect,url_for,flash,session, abort
from flask_sqlalchemy import SQLAlchemy
import sqlite3



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






@app.route('/')
def home():
	return render_template('index.html')


@app.route('/login')
def login():
	if session['logged_in']:
		return redirect(url_for('home'))

	return render_template('login.html')


@app.route('/signup')
def signup():
	if session['logged_in']:
		return redirect(url_for('home'))
	return render_template('signup.html')


@app.route('/userSignUp',methods=['POST'])
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


@app.route('/userLogin',methods=['POST','GET'])
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
@app.route('/logout')
def logout():
	session['logged_in']=False
	session['user_id']=''
	return redirect(url_for('home'))


if __name__ == '__main__' :
	app.run(debug=True)
	db.init_app(app)