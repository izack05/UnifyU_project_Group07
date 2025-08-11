from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length

# class RegistrationForm(FlaskForm):
#     id = StringField("Student ID", validators=[DataRequired(), Length(max=10)], render_kw={"placeholder": "Enter your student ID"})
#     full_name = StringField("Full Name", validators=[DataRequired(), Length(max=100)], render_kw={"placeholder": "Enter your full name"})
#     username = StringField("Username", validators=[DataRequired(), Length(max=10)], render_kw={"placeholder": "Enter your username"})
#     email = StringField("Email", validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email"})
#     password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "Enter your password"})
#     confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message="Passwords must match.")], render_kw={"placeholder": "Confirm your password"})
#     gender = RadioField("Gender", choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")], validators=[DataRequired()])
#     submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=10)], render_kw={"placeholder": "Enter your username"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)], render_kw={"placeholder": "Enter your password"})
    submit = SubmitField("Login")

    