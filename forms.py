from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class UserForm(FlaskForm):
    id = StringField("Student ID", validators=[DataRequired(), Length(max=10)], render_kw={"placeholder": "Enter your student ID"})
    full_name = StringField("Full Name", validators=[DataRequired(), Length(max=100)], render_kw={"placeholder": "Enter your full name"})
    username = StringField("Username", validators=[DataRequired(), Length(max=10)], render_kw={"placeholder": "Enter your username"})
    email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
    # password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "Enter your password"})
    # confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message="Passwords must match.")], render_kw={"placeholder": "Confirm your password"})
    gender = RadioField("Gender", choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")], validators=[DataRequired()])
    submit = SubmitField("Save Profile Info")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=10)], render_kw={"placeholder": "Enter your username"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField("Login")

#---------------Issue Form by [ Nur ]---------------------
class IssueLogForm(FlaskForm):
    issue_title = StringField("Issue Title", validators=[DataRequired(), Length(max=200)], 
                            render_kw={"placeholder": "Brief title of the issue"})
    issue_category = SelectField("Issue Category", 
                               choices=[
                                   ('Lab Computer', 'Lab Computer'),
                                   ('Network', 'Network/Internet'),
                                   ('Facilities', 'Facilities'),
                                   ('Other', 'Other')
                               ], 
                               validators=[DataRequired()])
    floor = SelectField("Floor", 
                       choices=[
                           ('B3', 'B3'), ('B2', 'B2'), ('B1', 'B1'), ('G', 'G'),
                           ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
                           ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
                           ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('FT', 'FT')
                       ],
                       validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired(), Length(max=100)],
                         render_kw={"placeholder": "Specific location on the floor (e.g., Room 302, North Wing)"})
    priority = SelectField("Priority",
                         choices=[
                             ('Low', 'Low'),
                             ('Medium', 'Medium'),
                             ('High', 'High'),
                             ('Critical', 'Critical')
                         ],
                         default='Medium',
                         validators=[DataRequired()])
    issue_description = TextAreaField("Issue Description", 
                                    validators=[DataRequired()], 
                                    render_kw={"placeholder": "Describe the issue in detail", "rows": 5})
    submit = SubmitField("Submit Issue")
