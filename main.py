from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3



app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////Desktip/saari/Aimup_app/aimup_app.db"
db = SQLAlchemy(app)

class Users(db.Model):
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
	return render_template('login.html')


@app.route('/signup')
def signup():
	return render_template('signup.html')
@app.route('/userSignUp',methods=['POST'])
def user_sign_up():
	email=request.form['email']
	first_name=request.form['first_name']
	last_name=request.form['last_name']
	password=request.form['password']

	create_user=Users(email=email,first_name=first_name,last_name=last_name,password=password)
	db.session.add(create_user)
	db.session.commit()
	

	return "sign up successful"



if __name__ == '__main__' :
	app.run(debug=True)