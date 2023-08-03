from wtforms import Form, StringField, DecimalField, TextAreaField, IntegerField, PasswordField, validators


class RegisterForm(Form):
    name = StringField('Full Name', [validators.Length(min=1, max=50)])
    username = StringField('User Name', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=10, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message="Password do not match!")])
    confirm = PasswordField('Confirm Password')
