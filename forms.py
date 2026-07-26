from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DecimalField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    

    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=50)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    submit = SubmitField("Create Account")

    from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    

    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=50)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    submit = SubmitField("Create Account")

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")   

class ExpenseForm(FlaskForm):

    amount = DecimalField("Amount ($)", validators=[DataRequired()])

    category = SelectField(
        "Category",
        choices=[
            ("Food", "Food"),
            ("Transport", "Transport"),
            ("Shopping", "Shopping"),
            ("Entertainment", "Entertainment"),
            ("Bills", "Bills"),
            ("Other", "Other")
        ]
    )

    description = StringField("Description")

    date = DateField("Date", validators=[DataRequired()])

    submit = SubmitField("Add Expense") 

