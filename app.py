from flask import Flask, request, render_template, redirect, request, flash, url_for, session, jsonify, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

from sk import flask_sk
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_seasurf import SeaSurf

from datetime import datetime, timezone
from decimal import Decimal

from forms import LoginForm

# A flask instance
app = Flask(__name__)

#create instance
db = SQLAlchemy()
# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
#Limiting the size of uploaded content to 16mb
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
#Initializing Database
db.init_app(app)
#secret key
app.secret_key = flask_sk

#CSRF protection
#csrf = SeaSurf(app)

login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view('login')


#-----------Model Template------------------------------- --> these are tables
# class Table_1(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Column1= db.Column(db.String(100), unique=True, nullable=False)
#     Column2= db.Column(db.String(250), nullable=False)
#     Column3= db.Column(db.String(500), nullable=False)


#Add all classes here
#---------Isaac classess--------------

class StudentRegistration(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name= db.Column(db.String(100), unique=False, nullable=False)
    username= db.Column(db.String(10), unique = True, nullable=False)
    email= db.Column(db.String(250), unique = True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    gender= db.Column(db.String(6), unique = False, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return StudentRegistration.query.get(user_id)


#----------Sariha classes---------------






#---------Sanjida classess--------------






#---------Nur classess------------------




#creating database
with app.app_context():
    db.create_all()



# Route decorators
#please make sure that you add @login_required decorator after every @app.route and before the funciton

#---------------Isaac Routes-----------------

@app.route("/")     #root URL

def index():
    return redirect('/login')
#     arr = ["Isaac", "Sariha", "Sanjida", "Nur"]
#     return render_template('index.html', array = arr)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = StudentRegistration.query.filter_by(username=form.username.data).first()
        if existing_user:
            if check_password_hash(existing_user.password, form.password.data):
                login_user(existing_user)
                return redirect('/homepage')
            else:
                flash('Wrong Password!', 'error')
                redirect('/login')
        else:
            flash('Username does not exist!', 'error')
            redirect('/login')

    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# @app.route("/user/<username>/<age>")   # this is a dynamic route --> you can pass anything at <username>
# def show_username(username, age):
#     return render_template('user.html', name=username, age = age)

# @app.route("/post/<int:post_id>")
# def show_post(post_id):
#     return f"Post id is {post_id}"


@app.route('/homepage')
@login_required
def homepage():
    
    # return render_template('home.html')
    return render_template('homepage.html')

@app.route('/registration')
def registration():
    return render_template("auth/registration.html")

@app.route('/student_registration', methods=["POST"])
def registration_student():
    student_id = request.form.get('id')
    username = request.form.get('username')
    email = request.form.get('email')

    id_exists = StudentRegistration.query.get(student_id)
    if id_exists:
        flash("Student ID already exists!", "error")
        return redirect('/registration')
    
    #username_exists = StudentRegistration.query.get(request.form.get('username'))
    username_exists = StudentRegistration.query.filter_by(username=username).first()
    if username_exists:
        flash("Username already exists!", "error")
        return redirect('/registration')
    
    #email_exists = StudentRegistration.query.get(request.form.get('email'))
    email_exists = StudentRegistration.query.filter_by(email=email).first()
    if email_exists:
        flash("An account has been created with this email already!", "error")
        return redirect('/registration')

    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash("Passwords do not match!", "error")
        return redirect('/registration')

    hashed_password = generate_password_hash(password)

    registered_student_row = StudentRegistration(
        id=request.form.get('id'), 
        full_name=request.form.get('fullname'), 
        username=request.form.get('username'), 
        email=request.form.get('email'), 
        password=hashed_password, 
        gender=request.form.get('gender')
    )
    db.session.add(registered_student_row)
    db.session.commit()

    flash("Registration successful!", "success")
    return redirect('/login')

@app.route('/getStudentRegistration_21201169')
def getStudent_21201169():
    result = db.session.execute(text('SELECT * FROM student_registration')).fetchall()
    result = [dict(row._mapping) for row in result]
    return jsonify(result)


#Error pages
#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
#Internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
#unauthorize error
@app.errorhandler(401)
def iunauthorized_error(e):
    return render_template('errors/401.html'), 401






#---------------Sariha Routes-----------------






#---------------Sanjida Routes-----------------





#---------------Nur Routes---------------------






#------------------------------end-----------------------------------------
if __name__ == '__main__':
    app.run(debug=True)   #helps us debug






#------------------useful methods/funcitons------------

#http methods
# @app.route("/submit", methods = ["GET", "POST"])
# def submit_data():
#     if request.method == "POST":
#         name=request.form.get('name')
#         age=request.form.get('age')

#         return f'Data submitted successfully! Name: {name}, age: {age}'
#     else:
#         return render_template("form.html")

#         #here below we do get request via url
#         # name = request.args.get("name")
#         # age = request.args.get("age")

#         # return f"Data Submitted via get, Name: {name} age: {age}"





#--------------------MORE NECESSARY THINGS THAT YOU CAN USE INSIDE CONTROLLER---------------------


# _---------------Add data in database from form (Insert)---------------------------

# @app.route('/register_url',methods=["POST"])
# def register_url():

#     Table_1_row=Table_1(Column1=request.form.get('form_field_name_1'),Column2=request.form.get('form_field_name_2'),Column3=request.form.get('form_field_name_3'))
#     db.session.add(Table_1_row)
#     db.session.commit()

#     return redirect('/reg_complete')   #url of the page you want to show after the registration is complete



#------------------Show data from Database (Select)----------------
# @app.route('/show_table')
# def show_table():
#    all_rows=Table1.query.all()
#    first_row=all_row[0]
#    specific_row=Table_1.query.filter_by(Column1="Rahim").first()
#    return render_template('home.html',data=specific_row)



#----------------------Update----------------
# @app.route('/update')
# def update():
#         specific_row=Table_1.query.filter_by(Column1="Robin").first()
#         specific_row.Column1="The new value you want to set in Column1"
#         specific_row.Column2="The new value you want to set in Column2"
#         specific_row.Column3="The new value you want to set in Column3"
        
#         db.session.commit()



#------------------------Delete---------------

# @app.route('/delete')
# def delete():
#         specific_row=Table_1.query.filter_by(Column1="Robin").first()
#         db.session.delete(specific_row)
#         db.session.commit()



#----------------Viewing in Postman------------------
# @app.route('/any_url')
# def any_url():
#     result = db.session.execute(text('SELECT * FROM students')).fetchall() #fetch the data you want to view using raw sql query
#     result = [dict(row._mapping) for row in result]
#     return jsonify(result)