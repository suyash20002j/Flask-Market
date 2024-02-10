from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, DataRequired, Email, ValidationError
from Market.models import User

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError("Username Already exists please try a different username.")
        
    def validate_email_address(self, email_to_check):
        user = User.query.filter_by(email_address = email_to_check.data).first()
        if user:
            raise ValidationError("Email already exists please try a different email_address.")

    username = StringField(label= 'Username : ', validators=[Length(min=2,max=30), DataRequired()])
    email_address = StringField(label = 'Email :', validators=[Email(), DataRequired()])
    password1 = PasswordField(label = 'Password : ', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label = 'Confirm Password :', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label = 'Create Account')


class LoginForm(FlaskForm):
    username = StringField(label= 'Username : ', validators=[DataRequired()])
    password = PasswordField(label = 'Password :', validators=[DataRequired()])
    submit = SubmitField(label = 'Sign In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label = 'Purchase the item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label = 'Sell Item')