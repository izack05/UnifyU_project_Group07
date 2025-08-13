from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField, SelectField
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
    issue_title = StringField("Issue Title", validators=[DataRequired(), Length(max=200)], render_kw={"placeholder": "Brief title of the issue"})
    issue_category = SelectField("Issue Category", 
                                choices=[
                                    ('Lab Computer', 'Lab Computer'),
                                    ('Network', 'Network/Internet'),
                                    ('Facilities', 'Facilities'),
                                    ('Other', 'Other')
                                ], 
                                validators=[DataRequired()])
    issue_description = TextAreaField("Issue Description", validators=[DataRequired()], render_kw={"placeholder": "Describe the issue in detail", "rows": 5})
    location = StringField("Location", validators=[DataRequired(), Length(max=100)], render_kw={"placeholder": "Building/Room (e.g., 10G32L, Library-2nd Floor)"})
    priority = SelectField("Priority", 
                          choices=[
                              ('Low', 'Low'),
                              ('Medium', 'Medium'),
                              ('High', 'High'),
                              ('Critical', 'Critical')
                          ], 
                          validators=[DataRequired()],
                          default='Medium')
    submit = SubmitField("Submit Issue")

    