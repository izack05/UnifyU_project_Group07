from flask import Flask, request, render_template, redirect, request, flash, url_for, session, jsonify, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

from sk import flask_sk
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_seasurf import SeaSurf

from datetime import datetime, timezone
from decimal import Decimal

from forms import LoginForm, UserForm, IssueLogForm

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
login_manager.login_view = 'login'
login_manager.login_message = "Please login to access this page!"
@login_manager.unauthorized_handler
def unauthorized():
    flash('Please login to access this page!', 'error')
    return redirect(url_for('login'))


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


#----------------------------------------------Sariha classes----------------------------------------------------------

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    logo = db.Column(db.String(200))             
    bio = db.Column(db.Text)                     
    rating = db.Column(db.Float, default=0.0)    
    members = db.Column(db.Integer, default=0) 
    events = db.relationship('Event', backref='club', lazy=True)

def seed_clubdata():
    if not Club.query.first():
        clubs = [
            Club(name='Computer Club', logo='computer.png', bio='A community for tech enthusiasts to collaborate on projects, participate in hackathons and share a skill space with the like-minded.', rating=4.8, members=450),
            Club(name='Research Club', logo='research.png', bio='A hub for curious minds to explore innovative ideas, collaborate on research projects, and engage in academic discussions across disciplines.', rating=4.2, members=422),
            Club(name='Cultural Club', logo='cultural.png', bio='A vibrant space to celebrate diverse traditions, showcase talents through events and performances, and promote cross-cultural understanding.', rating=4.9, members=320),
            Club(name='Book Club', logo='book.png', bio='A cozy community for bookworms to discover new reads, share insights, and dive into thought-provoking discussions.', rating=4.5, members=200),
        ]
        db.session.add_all(clubs)
        db.session.commit()

class clubapp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studid = db.Column(db.Integer, unique=True, nullable=False)
    email= db.Column(db.String(100), unique=True, nullable=False)
    phone= db.Column(db.Integer, unique=True, nullable=False)
    name= db.Column(db.String(500), nullable=False)
    interests=db.Column(db.String(500), nullable=False)
    skills=db.Column(db.String(500), nullable=False)

    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False) 
    club = db.relationship('Club', backref='applications')



class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False) 
    event_name = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_place = db.Column(db.String(100), nullable=False)
    event_about = db.Column(db.Text, nullable=False)








#---------Sanjida classess--------------






#---------Nur classess------------------
class IssueLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_registration.id'), nullable=False)
    issue_title = db.Column(db.String(200), nullable=False)
    issue_category = db.Column(db.String(50), nullable=False)  # Lab Computer, Network, Facilities, Other
    issue_description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)  # Building/Room location
    priority = db.Column(db.String(20), nullable=False, default='Medium')  # Low, Medium, High, Critical
    status = db.Column(db.String(20), nullable=False, default='Open')  # Open, In Progress, Resolved, Closed
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    resolved_at = db.Column(db.DateTime, nullable=True)
    staff_notes = db.Column(db.Text, nullable=True)
    
    # Relationship to student
    student = db.relationship('StudentRegistration', backref=db.backref('issues', lazy=True))





#creating database
with app.app_context():
    db.create_all()
    seed_clubdata()



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
    flash("You have been logged out", "success")
    return redirect('/login')

@app.route('/userprofile', methods = ['GET', 'POST'])
@login_required
def userprofile():
    form = UserForm()
    id = current_user.id
    name_to_update = StudentRegistration.query.get_or_404(id)

    if request.method == "POST":
        name_to_update.full_name = request.form['full_name']
        name_to_update.id = request.form['id']
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        name_to_update.gender = request.form['gender']

        try:
            db.session.commit()
            flash("User Info Updated Successfully!", "success")
            return render_template("profiles/UserProfile.html", form=form, name_to_update = name_to_update, id=id)
        except:
            flash("Error!  Looks like there was a problem...try again!", "error")
            return render_template("profiles/UserProfile.html", form=form, name_to_update = name_to_update, id=id)
    else:
        return render_template("profiles/UserProfile.html", form=form, name_to_update = name_to_update, id = id)
    
    return render_template("profiles/UserProfile.html")


# @app.route("/user/<username>/<age>")   # this is a dynamic route --> you can pass anything at <username>
# def show_username(username, age):
#     return render_template('user.html', name=username, age = age)

# @app.route("/post/<int:post_id>")
# def show_post(post_id):
#     return f"Post id is {post_id}"


@app.route('/homepage')
@login_required
def homepage():
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


@app.route('/homeclub')
@login_required
def homeclub():
    search_term = request.args.get('q', '').lower() 
    all_clubs = Club.query.all()

    if search_term:
        filtered_clubs = [club for club in all_clubs if 
            search_term in club.name.lower() or
            (club.bio and search_term in club.bio.lower())
        ]
    else:
        filtered_clubs = all_clubs

    return render_template('club/clubs.html', clubs=filtered_clubs)



@app.route('/clubs/<int:club_id>')
@login_required
def club_detail(club_id):
    club = Club.query.get_or_404(club_id)
    return render_template('club/club_detail.html', club=club)



@app.route('/apply_club/<int:club_id>', methods=['GET'])
@login_required
def apply_club_form(club_id):
    club = Club.query.get_or_404(club_id)
    return render_template('club/clubform.html', club=club)





@app.route('/apply_club/<int:club_id>', methods=['POST'])
@login_required
def register_student(club_id):
    club = Club.query.get_or_404(club_id)

    Student_row = clubapp(
        name=request.form.get('name'), 
        studid=request.form.get('studid'), 
        email=request.form.get("email"), 
        phone=request.form.get("phone"),
        interests=request.form.get("interests"),
        skills=request.form.get("skills")
    )
    Student_row.club_id = club.id 

    db.session.add(Student_row)
    db.session.commit()

    return redirect(url_for('club_detail', club_id=club.id))

@app.route('/addevent')
@login_required
def addevent():
    return render_template('club/addevent.html')

@app.route('/add-event', methods=['POST'])
@login_required
def add_event():

    event_date_str = request.form['event_date']
    event_date_obj = datetime.strptime(event_date_str, "%Y-%m-%d").date()

    new_event = Event(
        club_name=request.form.get('club_name'),
        event_name=request.form.get('event_name'),
        event_date=event_date_obj,
        event_place=request.form.get('event_place'),
        event_about=request.form.get('event_about')
    )

    db.session.add(new_event)
    db.session.commit()

    return redirect('/addevent')






#---------------Sanjida Routes-----------------





#---------------Nur Routes---------------------

# Route to display issue logging form and list user's issues
@app.route('/issues')
@login_required
def view_issues():
    # Get all issues for the current user
    user_issues = IssueLog.query.filter_by(student_id=current_user.id).order_by(IssueLog.submitted_at.desc()).all()
    return render_template('issues/view_issues.html', issues=user_issues)

# Route to create new issue
@app.route('/log_issue', methods=['GET', 'POST'])
@login_required
def log_issue():
    form = IssueLogForm()
    if form.validate_on_submit():
        new_issue = IssueLog(
            student_id=current_user.id,
            issue_title=form.issue_title.data,
            issue_category=form.issue_category.data,
            issue_description=form.issue_description.data,
            location=form.location.data,
            priority=form.priority.data
        )
        db.session.add(new_issue)
        db.session.commit()
        
        flash('Issue logged successfully! Our technical team will review it shortly.', 'success')
        return redirect(url_for('view_issues'))
    
    return render_template('issues/log_issue.html', form=form)

# Route to view individual issue details
@app.route('/issue/<int:issue_id>')
@login_required
def view_issue_detail(issue_id):
    issue = IssueLog.query.get_or_404(issue_id)
    
    # Ensure the user can only view their own issues
    if issue.student_id != current_user.id:
        flash('You can only view your own issues.', 'error')
        return redirect(url_for('view_issues'))
    
    return render_template('issues/issue_detail.html', issue=issue)







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