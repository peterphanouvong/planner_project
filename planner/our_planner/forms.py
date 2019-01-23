from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FloatField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from our_planner.models import User


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateField('Due date')
    submit = SubmitField('Done!')


class BudgetTrackerForm(FlaskForm):
    period = SelectField(
        'Tracking Period',
        choices=[('week', 'Weekly'), ('month', 'Monthly'), ('six', '6-Monthly'), ('year', 'Yearly')]
    )
    income_source = StringField('Income')
    income = FloatField('Income')
    expense_source = StringField('Expenses')
    expense = FloatField('Expenses')
    submit = SubmitField('Done!')

    def validate_income(self, income):
        if not income.isdigit():
            raise ValidationError("Please enter a valid number")

    def validate_expense(self, income):
        if not expense.isdigit():
            raise ValidationError("Please enter a valid number")


class RegistrationForm(FlaskForm):
    # first input to the form is the username, which will be called Username
    # it has restrictions, it must have some data, max 20 characters
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # putting in an email now
    email = StringField('Email', validators=[DataRequired(), Email()])
    # password field
    password = PasswordField('Password', validators=[DataRequired()])
    # passwork confirmation
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # submit button
    submit = SubmitField('Sign Up')

    secret_code = PasswordField('Secret Code')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Someone already has that username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Someone already has that email")


class LoginForm(FlaskForm):
    # putting in an email now
    email = StringField('Email', validators=[DataRequired(), Email()])
    # password field
    password = PasswordField('Password', validators=[DataRequired()])
    # to stay logged in
    remember = BooleanField('Remember Me')
    # submit button
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    # first input to the form is the username, which will be called Username
    # it has restrictions, it must have some data, max 20 characters
    username = StringField('Username', validators=[Length(min=2, max=20)])
    # putting in an email now
    email = StringField('Email', validators=[Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    # submit button
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Someone already has that username")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Someone already has that email")
