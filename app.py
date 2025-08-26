from flask import Flask, request, render_template, redirect, request, flash, url_for, session, jsonify, get_flashed_messages
from wtforms import BooleanField, TextAreaField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func, inspect
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail, Message

from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

from flask_migrate import Migrate

from sk import flask_sk, ai_key, DEL_EMAIL, MAIL_PASSWORD
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
#from flask_seasurf import SeaSurf

from datetime import datetime, timezone
from datetime import datetime, timedelta

from decimal import Decimal

from forms import LoginForm, UserForm, IssueLogForm

import os
import google.generativeai as genai
import json


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

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#for database change Migrations
migrate = Migrate(app, db) 


genai.configure(api_key=ai_key)

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









#-----------Mail-------------------#

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = DEL_EMAIL
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

mail=Mail(app)



#--------Club image--------#
UPLOAD_FOLDER = os.path.join("static", "logos")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



#-----------Model Template------------------------------- --> these are tables
# class Table_1(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Column1= db.Column(db.String(100), unique=True, nullable=False)
#     Column2= db.Column(db.String(250), nullable=False)
#     Column3= db.Column(db.String(500), nullable=False)


#Add all classes here
#---------Isaac classess--------------

@login_manager.user_loader
# def load_user(user_id):
#     return StudentRegistration.query.get(user_id)
def load_user(user_id):
    return db.session.get(StudentRegistration, int(user_id))


class StudentRegistration(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name= db.Column(db.String(100), unique=False, nullable=False)
    username= db.Column(db.String(10), unique = True, nullable=False)
    email= db.Column(db.String(250), unique = True, nullable=False)
    password = db.Column(db.String(255), nullable=False) 
    gender= db.Column(db.String(6), unique = False, nullable=False)
    is_verified = db.Column(db.Boolean, default = False)
    is_staff = db.Column(db.Boolean, default = False)
    is_admin = db.Column(db.Boolean, default = False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    

    # Relationships
    reported_issues = db.relationship(
        "IssueLog",
        foreign_keys="IssueLog.student_id",
        back_populates="student"
    )
    resolved_issues = db.relationship(
        "IssueLog",
        foreign_keys="IssueLog.resolved_by",
        back_populates="staff"
    )
    placed_orders = db.relationship('Order', back_populates='student', lazy=True)
    
    transactions = db.relationship('Transaction', back_populates='student', lazy='dynamic')


class StudentAdmin(ModelView):
    column_list = ('id', 'full_name', 'username', 'email', 'gender', 'is_verified', 'is_staff')
    form_columns = ('id','full_name', 'username', 'email', 'gender', 'password', 'is_verified', 'is_staff')
    form_excluded_columns = ()
    def on_model_change(self, form, model, is_created):
        # password hashing
        if model.password and not model.password.startswith('pbkdf2:'):
            model.password = generate_password_hash(model.password)

class AddAdmin(ModelView):
    column_list = ('id',  'is_admin', 'full_name', 'username', 'email')
    form_columns = ('id',  'is_admin', 'full_name', 'username', 'email', 'password')
    form_excluded_columns = ()
    can_delete = False
    def on_model_change(self, form, model, is_created):
        # password hashing
        if model.password and not model.password.startswith('pbkdf2:'):
            model.password = generate_password_hash(model.password)




#----------------------------------------------Sariha classes----------------------------------------------------------

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    logo = db.Column(db.String(200))             
    bio = db.Column(db.Text)                     
    rating = db.Column(db.Float, default=0.0)    
    members = db.Column(db.Integer, default=0) 
    email = db.Column(db.String(250))
    events = db.relationship('Event', backref='club', lazy=True)

def seed_clubdata():
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('club')]
    if 'email' not in columns:
        return
    if not Club.query.first():
        clubs = [
            Club(name='Computer Club', logo='computer.png', bio='A community for tech enthusiasts to collaborate on projects, participate in hackathons and share a skill space with the like-minded.', rating=4.8, members=450, email='computerclub.unifyu@gmail.com'),
            Club(name='Research Club', logo='research.png', bio='A hub for curious minds to explore innovative ideas, collaborate on research projects, and engage in academic discussions across disciplines.', rating=4.2, members=422, email='research@gmail.com'),
            Club(name='Cultural Club', logo='cultural.png', bio='A vibrant space to celebrate diverse traditions, showcase talents through events and performances, and promote cross-cultural understanding.', rating=4.9, members=320, email='cultural@gmail.com'),
            Club(name='Book Club', logo='book.png', bio='A cozy community for bookworms to discover new reads, share insights, and dive into thought-provoking discussions.', rating=4.5, members=200, email='bookclub.unifyu@gmail.com'),
        ]
        db.session.add_all(clubs)
        db.session.commit()

class clubapp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studid = db.Column(db.Integer, nullable=False)
    email= db.Column(db.String(100), nullable=False)
    phone= db.Column(db.Integer, nullable=False)
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

class StudyPodBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('student_registration.id'), nullable=False)
    
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    study_pod = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(20), nullable=False)
    
    user = db.relationship('StudentRegistration', backref=db.backref('bookings', lazy=True))
    
    __table_args__ = (
        db.UniqueConstraint('study_pod', 'date', 'time_slot', name='unique_pod_booking'),
    )




class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    image = db.Column(db.String(200))
    category = db.Column(db.String(50), nullable=False)  # NEW

class FoodItemAdmin(ModelView):
    column_list = ('id', 'name', 'price', 'stock', 'category')
    column_searchable_list = ('name', 'category')
    column_filters = ('category', 'price')
    form_columns = ('name', 'price', 'stock', 'description', 'image', 'category')
    form_overrides = {
        'description': TextAreaField
    }

def seed_fooddata():
    if not FoodItem.query.first():  # only seed if empty
        foods = [
            # Snacks
            FoodItem(name="Vegetable Shingara", price=10, stock=50,
                     description="Crispy fried shingara", image="shingara.jpg", category="Snacks"),
            FoodItem(name="Chicken Samosa", price=10, stock=40,
                     description="Spicy chicken samosa", image="samosa.jpg", category="Snacks"),
            FoodItem(name="Chicken Shawarma", price=80, stock=25,
                     description="Juicy chicken shawarma", image="shawarma.jpg", category="Snacks"),
            FoodItem(name="Fuchka", price=60, stock=50,
                     description="Mouthwatering Fuchka", image="fuchka.jpg", category="Snacks"),
            FoodItem(name="Chicken Burger", price=80, stock=40,
                     description="Crispy chicken burger", image="chicken_burger.jpg", category="Snacks"),
            
            # Rice
            FoodItem(name="Plain Rice", price=20, stock=100,
                     description="Steamed plain rice", image="plain_rice.jpg", category="Rice"),
            FoodItem(name="Fried Rice", price=50, stock=80,
                     description="Fried rice with vegetables", image="fried_rice.jpg", category="Rice"),
            FoodItem(name="Khichuri", price=60, stock=70,
                     description="Traditional khichuri", image="khichuri.jpg", category="Rice"),
            FoodItem(name="Beef Tehari", price=120, stock=40,
                     description="Spicy beef tehari", image="beef_tehari.jpg", category="Rice"),
            FoodItem(name="Chicken Biryani", price=100, stock=50,
                     description="Delicious chicken biryani", image="chicken_biryani.jpg", category="Rice"),

            # Pasta & Noodles
            FoodItem(name="Pasta", price=70, stock=40,
                     description="Creamy pasta", image="pasta.jpg", category="Pasta & Noodles"),
            FoodItem(name="Chowmein", price=60, stock=60,
                     description="Stir-fried chowmein", image="chowmein.jpg", category="Pasta & Noodles"),

            # Chicken
            FoodItem(name="Chicken Curry", price=90, stock=50,
                     description="Spicy chicken curry", image="chicken_curry.jpg", category="Chicken"),
            FoodItem(name="Chicken Fry", price=80, stock=40,
                     description="Crispy chicken fry", image="chicken_fry.jpg", category="Chicken"),
            FoodItem(name="Chilli Chicken", price=100, stock=30,
                     description="Hot chilli chicken", image="chilli_chicken.jpg", category="Chicken"),
        ]
        db.session.add_all(foods)
        db.session.commit()

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=5000.0)

    student_id = db.Column(db.Integer, db.ForeignKey('student_registration.id', name='fk_BankAccount_student'), unique=True)
    student = db.relationship('StudentRegistration', backref=db.backref('bank_account', uselist=False))

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_registration.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'credit' or 'debit'
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))  # e.g., "Canteen: Sandwich x 2"
    date = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('StudentRegistration', back_populates='transactions')

#---------Nur classess------------------
class IssueLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_registration.id', name='fk_issue_log_student'), nullable=False)
    issue_title = db.Column(db.String(200), nullable=False)
    issue_category = db.Column(db.String(50), nullable=False)
    issue_description = db.Column(db.Text, nullable=False)
    floor = db.Column(db.String(3), nullable=False, default='1')
    location = db.Column(db.String(100), nullable=False)
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    status = db.Column(db.String(20), nullable=False, default='Reported')
    submitted_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    resolved_at = db.Column(db.DateTime, nullable=True)
    staff_notes = db.Column(db.Text, nullable=True)
    resolved_by = db.Column(db.Integer, db.ForeignKey('student_registration.id', name='fk_issue_log_resolved_by'), nullable=True)
    is_new = db.Column(db.Boolean, nullable=False, default=True)  # New: track if issue is new for staff

    # student = db.relationship('StudentRegistration', backref=db.backref('issues', lazy=True), foreign_keys=[student_id])
    # staff = db.relationship('StudentRegistration', backref=db.backref('resolved_issues', lazy=True), foreign_keys=[resolved_by])

    

    student = db.relationship(
        'StudentRegistration',
        foreign_keys=[student_id],
        back_populates="reported_issues"
    )
    staff = db.relationship(
        'StudentRegistration',
        foreign_keys=[resolved_by],
        back_populates="resolved_issues"
    )



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer, 
        db.ForeignKey('student_registration.id', name='fk_order_student'), 
        nullable=False
    )

    invoice_data = db.Column(db.Text, nullable=False)  
    total = db.Column(db.Float, nullable=False)      

    status = db.Column(db.String(20), nullable=False, default='Pending') 
    placed_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    completed_at = db.Column(db.DateTime, nullable=True)
    student = db.relationship(
        'StudentRegistration',
        back_populates='placed_orders',
        lazy=True
    )






#creating database
with app.app_context():
    db.create_all()

    seed_clubdata()
    seed_fooddata()

#--------------------------------admin panel stuff-------------------------------------------------
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return url_for("homepage")
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("homepage"))
    @expose("/")
    def index(self):
        admins = StudentRegistration.query.filter_by(is_admin=True).all()

        # user type count
        total =  db.session.query(func.count(StudentRegistration.id)).scalar()
        admin_count = db.session.query(func.count(StudentRegistration.id)).filter_by(is_admin=True).scalar()
        staff_count = db.session.query(func.count(StudentRegistration.id)).filter_by(is_staff=True).scalar()
        student_count = total - (admin_count + staff_count)
        verified_student_count = db.session.query(func.count(StudentRegistration.id)).filter_by(is_verified=True).scalar()
        unverified_student_count = db.session.query(func.count(StudentRegistration.id)).filter_by(is_verified=False).scalar()

        #club info counts
        clubs = Club.query.order_by(Club.name).all()
        club_names = []
        club_member_count = []  
        for club in clubs:
            club_names.append(club.name)
            club_member_count.append(club.members)
        max_club_members = max(club_member_count)

        #club application count by clubs
        application_counts = (
                db.session.query(clubapp.club_id, func.count(clubapp.id))
                .group_by(clubapp.club_id)
                .all()
            )
        
        club_app_name = []
        club_app_count = []
        for club_id, count in application_counts:
            club = Club.query.get(club_id)
            if club:
                club_app_name.append(club.name)
                club_app_count.append(count)

        # issue-log-status count
        reported_count = db.session.query(func.count(IssueLog.id)).filter_by(status="Reported").scalar()
        on_process_count = db.session.query(func.count(IssueLog.id)).filter_by(status="On Process").scalar()
        solved_count = db.session.query(func.count(IssueLog.id)).filter_by(status="Solved").scalar()

        # cafe food stock count
        fooditems = FoodItem.query.order_by(FoodItem.name).all()
        fooditem_names = []
        fooditem_stock = []
        for item in fooditems:
            fooditem_names.append(item.name)
            fooditem_stock.append(item.stock)
        max_stock_number = max(fooditem_stock)
        

        return self.render(
            "admin/index.html",
            admins = admins,
            total = total, 
            admin_count = admin_count,
            staff_count = staff_count,
            student_count = student_count,
            verified_students_count = verified_student_count,
            unverified_students_count = unverified_student_count,

            club_names = club_names,
            club_member_count = club_member_count,
            max_club_members = max_club_members + 50,

            club_app_name = club_app_name,
            club_app_count = club_app_count,

            reported=reported_count,
            on_process=on_process_count,
            solved=solved_count,

            fooditem_names = fooditem_names,
            fooditem_stock = fooditem_stock,
            max_stock_number = max_stock_number + 50
        )
    

    

class MyButtonsView(BaseView):
    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/club_buttons.html')

    

# class StudentRegistrationView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/studentregister.html', endpoint='users')

admin = Admin(name="Admin Panel", template_mode='bootstrap4', index_view = MyAdminIndexView())
admin.init_app(app)
admin.add_view(StudentAdmin(StudentRegistration, db.session, name="Users", endpoint="users_list")) 
admin.add_view(FoodItemAdmin(FoodItem, db.session, name="Food Items"))
admin.add_view(MyButtonsView(name="Club Actions", endpoint="actions"))
admin.add_view(AddAdmin(StudentRegistration, db.session, name="Add/Remove Admin", endpoint="add_admin"))



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
        #name_to_update.id = request.form['id']
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
    
    if len(password) < 6:
        flash("Password length cannot be less than 6 Characters", "error")
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

    new_bank = BankAccount(
        name=registered_student_row.full_name,
        email=registered_student_row.email,
        balance=5000.0,
        student_id=registered_student_row.id
    )

    db.session.add(new_bank)

    db.session.commit()

    flash("Registration successful!", "success")
    return redirect('/login')

@app.route('/getStudentRegistration_21201169')
def getStudent_21201169():
    result = db.session.execute(text('SELECT * FROM student_registration')).fetchall()
    result = [dict(row._mapping) for row in result]
    return jsonify(result)

#Admin page
# @app.route('/admin')
# @login_required
# def admin():
#     id = current_user.id
#     if id == 12345678:
#         return render_template("admin/admin.html")
#     else:
#         flash("Only Admin Has Access Here",'error')
#         return redirect(url_for('homepage'))


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



@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    interest = data.get("interest", "")

    #Fetch all clubs from database
    clubs = Club.query.all()
    clubs_list = "\n".join([f"{c.name}: {c.bio}" for c in clubs])

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
        The student says: "{interest}".
        
        Available clubs:
        {clubs_list}

        Your job:
        - If you find relevant clubs, reply ONLY in this format: 
          "Hey! Based on your interests you might like to check out [club names]."
        - If the interest is vague or weakly related, reply: 
          "Hey, we think you'd might like these clubs: [club names]."
        - If nothing matches at all or the input is nonsense, reply: 
          "Sorry! Couldn't recommend a club, do browse and see what you like!"
        - Keep the reply short and conversational. No extra text.
        """

        response = model.generate_content(prompt)
        return jsonify({"recommendation": response.text.strip()})

    except Exception as e:
        return jsonify({"recommendation": f"Sorry, error: {str(e)}"})


@app.route('/apply_club/<int:club_id>', methods=['GET'])
@login_required
def apply_club_form(club_id):
    club = Club.query.get_or_404(club_id)
    student = StudentRegistration.query.filter_by(id=current_user.id).first_or_404()
    return render_template('club/clubform.html', club=club, student=student)





@app.route('/apply_club/<int:club_id>', methods=['POST'])
@login_required
def register_student(club_id):
    club = Club.query.get_or_404(club_id)
    student = StudentRegistration.query.filter_by(id=current_user.id).first_or_404()

    Student_row = clubapp(
        name=student.full_name,
        studid=student.id,
        email=request.form.get('email'),
        phone=request.form.get("phone"),
        interests=request.form.get("interests"),
        skills=request.form.get("skills")
    )
    Student_row.club_id = club.id 

    db.session.add(Student_row)
    db.session.commit()

    return redirect(url_for('club_detail', club_id=club.id))

@app.route('/show_club_applications')
@login_required
def show_club_applications():
    if not current_user.is_admin:
        return redirect(url_for("homepage"))

    applications = clubapp.query.join(clubapp.club).order_by(Club.name, clubapp.name).all()
    return render_template('club/view_clubapp.html', applications=applications)


@app.route('/addevent')
@login_required
def addevent():
    if not (current_user.is_authenticated and current_user.is_admin):
        return redirect(url_for('homepage'))
    clubs = Club.query.all()
    if not clubs:
        return redirect(url_for('homeclub'))
    return render_template('club/addevent.html', clubs=clubs)


@app.route('/add-event', methods=['POST'])
@login_required
def add_event():

    club_id_str = request.form.get('club_id')
    if not club_id_str:
        return redirect(url_for('addevent'))

    try:
        club_id = int(club_id_str)
    except ValueError:
        return redirect(url_for('addevent'))

    event_date_str = request.form.get('event_date')
    try:
        event_date_obj = datetime.strptime(event_date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return redirect(url_for('addevent'))

    new_event = Event(
        club_id=club_id,
        event_name=request.form.get('event_name'),
        event_date=event_date_obj,
        event_place=request.form.get('event_place'),
        event_about=request.form.get('event_about')
    )

    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for('club_detail', club_id=club_id))



@app.route('/balance')
@login_required
def balance():
    student = StudentRegistration.query.get(current_user.id)
    if not student:
        flash("Student not found!", "error")
        return redirect(url_for('homepage'))
    bank = student.bank_account  # still needed for add/withdraw
    return render_template('club/user_balance.html', student=student, bank=bank)


@app.route('/admin/clubs')
@login_required
def admin_view_club():
    if not current_user.is_admin:
        return redirect(url_for('homepage'))

    clubs = Club.query.order_by(Club.name).all()
    return render_template('admin/clubs_list.html', clubs=clubs)




@app.route('/admin/club', methods=['GET', 'POST'])
@app.route('/admin/club/<int:club_id>', methods=['GET', 'POST'])
@login_required
def manage_club(club_id=None):
    if not current_user.is_admin:
        return redirect(url_for('homepage'))

    club = Club.query.get(club_id) if club_id else Club()

    if request.method == 'POST':
        club.name = request.form['name']
        club.bio = request.form.get('bio')
        club.rating = float(request.form.get('rating') or 0)
        club.members = int(request.form.get('members') or 0)
        club.email = request.form.get('email')

        # Handle file upload
        logo_file = request.files.get('logo')
        if logo_file and logo_file.filename:
            filename = secure_filename(logo_file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            logo_file.save(save_path)
            club.logo = f"logos/{filename}"   # save relative path

        db.session.add(club)
        db.session.commit()
        return redirect(url_for('admin_view_club'))

    return render_template('admin/manage_club_form.html', club=club)


@app.route('/admin/club/delete/<int:club_id>', methods=['POST'])
@login_required
def delete_club(club_id):
    if not current_user.is_admin:
        return redirect(url_for('homepage'))

    club = Club.query.get_or_404(club_id)

    events = Event.query.filter_by(club_id=club.id).all()
    for event in events:
        db.session.delete(event)

    db.session.delete(club)
    db.session.commit()
    return redirect(url_for('admin_view_club'))


@app.route("/send_applications", methods=["POST"])
@login_required
def send_applications():
    app_ids = request.form.getlist("app_ids")
    applications = clubapp.query.filter(clubapp.id.in_(app_ids)).all()

    if not applications:
        return redirect(url_for("show_club_applications"))

   
    club_email = applications[0].club.email  


    body = ""
    for app in applications:
        body += f"""
Student Name: {app.name}
Student ID: {app.studid}
Email: {app.email}
Phone: {app.phone}
Interests: {app.interests}
Skills: {app.skills}
Club: {app.club.name}
-----------------------
"""


    msg = Message(
        subject="New Club Applications",
        sender=DEL_EMAIL,
        recipients=[club_email] 
    )
    msg.body = body
    mail.send(msg)

    for app in applications:
        db.session.delete(app)
    db.session.commit()

    return redirect(url_for("show_club_applications"))












#---------------Sanjida Routes-----------------

@app.route('/library_home')
@login_required
def library_home():
    today = datetime.today().date()
    dates = [today, today + timedelta(days=1), today + timedelta(days=2)]

    date_strs = [d.strftime('%d/%m/%Y') for d in dates]

    booked_slots = StudyPodBooking.query.filter(
        StudyPodBooking.study_pod.in_([
            "Individual Pod 1",
            "Individual Pod 2",
            "Group Pod 1",
            "Group Pod 2"
        ]),
        StudyPodBooking.date.in_(dates)
    ).all()

    booked = {}
    for b in booked_slots:
        key = (b.study_pod, b.date.strftime('%d/%m/%Y'))
        booked.setdefault(key, []).append(b.time_slot)

    return render_template(
        "library/library_home.html",
        booked=booked,
        dates=date_strs
    )

@app.route('/studypod_bookingform')
@login_required
def studypod_bookingform():
    today = datetime.today()
    min_date = today.strftime('%Y-%m-%d')
    max_date = (today + timedelta(days=3)).strftime('%Y-%m-%d')
    return render_template("library/studypod_bookingform.html", min_date=min_date, max_date=max_date)

@app.route('/book_study_pod', methods=['POST'])
@login_required
def studypod_booking():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    study_pod = request.form.get('study_pod')
    date_str = request.form.get('date')
    time_slot = request.form.get('time_slot')

    if not all([fullname, email, study_pod, date_str, time_slot]):
        flash("Please fill in all the fields.", "error")
        return redirect(url_for('studypod_bookingform'))

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash("Invalid date format.", "error")
        return redirect(url_for('studypod_bookingform'))

    today = datetime.today().date()
    if selected_date < today or selected_date > today + timedelta(days=3):
        flash("Selected date is out of allowed booking range.", "error")
        return redirect(url_for('studypod_bookingform'))

    existing_booking = StudyPodBooking.query.filter_by(
        study_pod=study_pod,
        date=selected_date,
        time_slot=time_slot
    ).first()

    if existing_booking:
        flash("This study pod is already booked for the selected date and time slot.", "error")
        return redirect(url_for('studypod_bookingform'))

    booking = StudyPodBooking(
        user_id=current_user.id,
        fullname=fullname,
        email=email,
        study_pod=study_pod,
        date=selected_date,
        time_slot=time_slot
    )
    db.session.add(booking)
    db.session.commit()

    # Redirect to invoice page
    return redirect(url_for('studypod_invoice', booking_id=booking.id))

@app.route('/studypod_invoice/<int:booking_id>')
@login_required
def studypod_invoice(booking_id):
    booking = StudyPodBooking.query.get_or_404(booking_id)
    return render_template("library/studypod_invoice.html", booking=booking)



from collections import defaultdict




@app.route('/canteen')
def canteen_home():
    # Fetch all items
    items = FoodItem.query.all()

    # Get filters from query params
    selected_category = request.args.get('category', '').strip()
    search_query = request.args.get('q', '').strip().lower()
    min_price = request.args.get('min_price', '').strip()
    max_price = request.args.get('max_price', '').strip()

    # Convert price filters to float if possible
    try:
        min_price = float(min_price) if min_price else None
    except ValueError:
        min_price = None

    try:
        max_price = float(max_price) if max_price else None
    except ValueError:
        max_price = None

    # Group items by category after filtering
    grouped_items = defaultdict(list)
    for item in items:
        # Search filter
        if search_query and not (search_query in item.name.lower() or (item.description and search_query in item.description.lower())):
            continue

        # Price filter
        if (min_price is not None and item.price < min_price) or (max_price is not None and item.price > max_price):
            continue

        # Category filter (applied later globally)
        grouped_items[item.category].append(item)

    # Apply category filter if selected
    categories = list(grouped_items.keys())
    if selected_category and selected_category in categories:
        filtered_grouped = defaultdict(list)
        filtered_grouped[selected_category] = grouped_items[selected_category][:]
        grouped_items = filtered_grouped
        categories = [selected_category]
    else:
        selected_category = ""

    # Cart info
    cart = session.get('cart', [])
    total_quantity = sum(item['quantity'] for item in cart)

    return render_template(
        'canteen/canteen_home.html',
        grouped_items=grouped_items,
        cart=cart,
        total_quantity=total_quantity,
        categories=categories,
        selected_category=selected_category,
        search_query=search_query,
        min_price=min_price,
        max_price=max_price
    )


@app.route('/canteen_item/<int:food_id>', methods=['POST'])
@login_required
def canteen_item(food_id):
    item = FoodItem.query.get_or_404(food_id)
    action = request.form.get('action')  # 'increase', 'decrease', 'add'
    key = f'temp_qty_{food_id}'
    qty = session.get(key, 0)

    if action == 'increase':
        qty = min(qty + 1, item.stock)
    elif action == 'decrease' and qty > 0:
        qty -= 1
    elif action == 'add':
        if qty <= 0:
            flash(f"⚠️ Please select a quantity for {item.name}.", "warning")
        else:
            # Add to cart
            cart = session.get('cart', [])
            cart_item = next((c for c in cart if c['id'] == item.id), None)
            if cart_item:
                cart_item['quantity'] = min(cart_item['quantity'] + qty, item.stock)
            else:
                cart.append({
                    'id': item.id,
                    'name': item.name,
                    'price': item.price,
                    'quantity': min(qty, item.stock)
                })
            session['cart'] = cart
            flash(f"✅ {item.name} added to cart!", "success")
        qty = 0  # reset temp counter after adding

    session[key] = qty
    return redirect(request.referrer or url_for('canteen_home'))

@app.route('/update_cart/<int:food_id>', methods=['POST'])
@login_required
def update_cart(food_id):
    action = request.form.get('action')  # 'increase', 'decrease', 'remove'
    cart = session.get('cart', [])

    for item in cart:
        if item['id'] == food_id:
            if action == 'increase':
                item['quantity'] += 1
            elif action == 'decrease':
                item['quantity'] -= 1
                if item['quantity'] <= 0:
                    cart.remove(item)
            elif action == 'remove':
                cart.remove(item)
            break

    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart')
@login_required
def cart():
    cart = session.get('cart', [])
    # Ensure all quantities ≥ 1
    for item in cart:
        if 'quantity' not in item or item['quantity'] < 1:
            item['quantity'] = 1

    session['cart'] = cart
    total = sum(item['price'] * item['quantity'] for item in cart)

    return render_template('canteen/cart.html', cart=cart, total=total)

@app.route('/invoice')
@login_required
def invoice():
    last_order = session.get('last_order')
    if not last_order:
        flash("❌ No recent order found.", "danger")
        return redirect(url_for('canteen_home'))

    items = last_order['items']
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    total = last_order['total']

    return render_template('canteen/invoice.html', items=items, subtotal=subtotal, total=total)

@app.route('/confirm_order', methods=['POST'])
@login_required
def confirm_order():
    cart = session.get('cart', [])
    if not cart:
        flash("⚠️ Your cart is empty.", "danger")
        return redirect(url_for('cart'))
    
    student = StudentRegistration.query.get(current_user.id)
    if not student:
        return redirect(url_for('cart'))
    
    total = sum(item['price'] * item['quantity'] for item in cart)

    if student.balance < total:
        flash("⚠️ Insufficient balance. Please top up first.", "warning")
        return redirect(url_for('cart'))

    # Deduct stock
    for item in cart:
        food_item = FoodItem.query.get(item['id'])
        if food_item and food_item.stock >= item['quantity']:
            food_item.stock -= item['quantity']
            db.session.add(food_item)
        else:
            flash(f"⚠️ Not enough stock for {item['name']}.", "warning")
            return redirect(url_for('cart'))
        
    # Deduct student balance
    student.balance -= total
    db.session.add(student)

    # Log **canteen purchase as transaction**
    for item in cart:
        txn = Transaction(
            student_id=student.id,
            type='debit',  # money spent
            amount=item['price'] * item['quantity'],
            description=f"Canteen: {item['name']} x {item['quantity']}"
        )
        db.session.add(txn)

    # Save order for invoice
    order = Order(
        student_id=student.id,
        invoice_data=json.dumps(cart),  
        total=total
    )
    db.session.add(order)

    db.session.commit()

    # Save last order in session for invoice
    session['last_order'] = {
        'items': cart.copy(),
        'total': total
    }

    # Clear cart
    session['cart'] = []

    flash("✅ Order confirmed successfully!", "success")
    return redirect(url_for('invoice'))


@app.route('/balance/add', methods=['GET', 'POST'])
@login_required
def add_credit():
    student = StudentRegistration.query.get(current_user.id)

    # Auto-create bank account if missing
    bank = student.bank_account
    if not bank:
        bank = BankAccount(
            name=student.full_name,
            email=student.email,
            balance=5000.0,  # default starting balance
            student_id=student.id
        )
        db.session.add(bank)
        db.session.commit()

    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
        except ValueError:
            flash("Invalid input.", "warning")
            return render_template('balance/add_credit.html', student=student, bank=bank)

        if amount <= 0:
            flash("Enter a valid positive amount.", "warning")
        elif amount > bank.balance:
            flash("Bank doesn't have enough balance.", "warning")
        else:
            # Update balances
            student.balance += amount
            bank.balance -= amount

            # Log transaction
            txn = Transaction(student_id=student.id, type='credit', amount=amount)
            db.session.add(txn)
            db.session.commit()

            flash(f"{amount} ৳ added successfully!", "success")

    return render_template('balance/add_credit.html', student=student, bank=bank)


@app.route('/balance/withdraw', methods=['GET', 'POST'])
@login_required
def withdraw_credit():
    student = StudentRegistration.query.get(current_user.id)
    bank = student.bank_account

    if not student or not bank:
        flash("Bank account not found!", "error")
        return redirect(url_for('balance'))

    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
        except ValueError:
            flash("Invalid input.", "warning")
            return render_template('balance/withdraw_credit.html', student=student, bank=bank)

        if amount <= 0:
            flash("Enter a valid positive amount.", "warning")
        elif amount > student.balance:
            flash("You don't have enough balance to withdraw.", "warning")
        else:
            # Update balances
            student.balance -= amount
            bank.balance += amount

            # Log transaction
            txn = Transaction(student_id=student.id, type='withdraw', amount=amount)
            db.session.add(txn)
            db.session.commit()

            flash(f"{amount} ৳ has been withdrawn successfully!", "success")

    return render_template('balance/withdraw_credit.html', student=student, bank=bank)

@app.route('/balance/history')
@login_required
def transaction_history():
    student = StudentRegistration.query.get(current_user.id)
    transactions = student.transactions.order_by(Transaction.date.desc()).all()
    return render_template('balance/history.html', transactions=transactions)

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
            floor=form.floor.data,
            location=form.location.data,
            priority=form.priority.data,
            status='Reported',
            is_new=True  # Mark as new for staff
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

@app.route('/staff/issues')
@login_required
def staff_issues():
    if not current_user.is_staff:
        flash('Access denied. Staff only area.', 'error')
        return redirect(url_for('homepage'))

    floor = request.args.get('floor', 'ALL')

    if floor != 'ALL':
        issues = IssueLog.query.filter_by(floor=floor).all()
    else:
        issues = IssueLog.query.all()

    reported = [i for i in issues if i.status == 'Reported']
    on_process = [i for i in issues if i.status == 'On Process']
    solved = [i for i in issues if i.status == 'Solved']

    # Count new issues for notification
    new_issues_count = IssueLog.query.filter_by(is_new=True, status='Reported').count()

    return render_template('issues/staff_issues.html',
                         reported=reported,
                         on_process=on_process,
                         solved=solved,
                         selected_floor=floor,
                         new_issues_count=new_issues_count)

@app.route('/staff/update_issue_status', methods=['POST'])
@login_required
def update_issue_status():
    if not current_user.is_staff:
        return jsonify({'error': 'Access denied'}), 403

    issue_id = request.form.get('issue_id')
    new_status = request.form.get('status')
    staff_notes = request.form.get('staff_notes', '')

    issue = IssueLog.query.get_or_404(issue_id)
    # Only allow forward status transitions
    allowed_transitions = {
        'Reported': ['On Process', 'Solved'],
        'On Process': ['Solved'],
        'Solved': []
    }
    if new_status not in allowed_transitions.get(issue.status, []):
        return jsonify({'error': 'Invalid status transition'}), 400

    issue.status = new_status
    issue.staff_notes = staff_notes
    if new_status == 'Solved':
        issue.resolved_at = datetime.now()
        issue.resolved_by = current_user.id
    if new_status == 'On Process':
        issue.resolved_at = datetime.now()
        issue.resolved_by = current_user.id# Mark as not new if status is updated
    issue.is_new = False

    db.session.commit()

    return jsonify({'success': True})

@app.route('/staff/issue/<int:issue_id>')
@login_required
def staff_issue_detail(issue_id):
    if not current_user.is_staff:
        flash('Access denied. Staff only area.', 'error')
        return redirect(url_for('homepage'))

    issue = IssueLog.query.get_or_404(issue_id)
    # Mark as not new if staff views details
    if issue.is_new:
        issue.is_new = False
        db.session.commit()
    return render_template('issues/staff_issue_detail.html', issue=issue)
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