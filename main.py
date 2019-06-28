from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/aimup_app"
db = SQLAlchemy(app)

@app.route('/')
def home():
	return render_template('index.html')


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/signup')
def signup():
	return render_template('signup.html')



if __name__ == '__main__' :
	app.run(debug=True)