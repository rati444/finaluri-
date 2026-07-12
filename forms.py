from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from choices import SUBJECT_CHOICES, SEMESTER_CHOICES, RESOURCE_TYPE_CHOICES


class RegisterForm(FlaskForm):
    full_name = StringField("სახელი და გვარი", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("ელფოსტა", validators=[DataRequired(), Email()])
    password = PasswordField("პაროლი", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "გაიმეორეთ პაროლი",
        validators=[DataRequired(), EqualTo("password", message="პაროლები არ ემთხვევა.")],
    )
    submit = SubmitField("რეგისტრაცია")


class LoginForm(FlaskForm):
    email = StringField("ელფოსტა", validators=[DataRequired(), Email()])
    password = PasswordField("პაროლი", validators=[DataRequired()])
    submit = SubmitField("შესვლა")


class ResourceForm(FlaskForm):
    title = StringField("სათაური", validators=[DataRequired(), Length(min=2, max=200)])
    subject = SelectField("საგანი", choices=SUBJECT_CHOICES, validators=[DataRequired()])
    semester = SelectField("სემესტრი", choices=SEMESTER_CHOICES, validators=[DataRequired()])
    resource_type = SelectField("ტიპი", choices=RESOURCE_TYPE_CHOICES, validators=[DataRequired()])
    submit = SubmitField("დამატება")
