from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField,SubmitField,RadioField,PasswordField
from wtforms.validators import DataRequired, Email,Length


#Ask Question Form Field
class AskQuestionForm(FlaskForm):
  """
  Handles Question Form Field
  """
  question_title = StringField("Question", validators=[DataRequired(message="Enter between 2 and 50 characters"),Length(min=2, max=50)])
  subject_category = SelectField("Subject Category",choices=[
    ("mathematics","Mathematics"),
    ("chemistry","Chemistry"),
    ("igbo","Igbo"),
    ("physics","Physics"),
    ("digital technology","Digital Technology"),
  ],validators=[DataRequired(message="Subject is needed")])
  question_details = TextAreaField("Question in Details",validators=[DataRequired(message="Enter between 2 and 180 characters"),Length(min=2, max=180)])
  submit = SubmitField("Save Question")


#Answer section
class AnswerForm(FlaskForm):
  """
  Users can post answers here
  """
  answer = TextAreaField("Post Answer Here",validators=[DataRequired(message="Characters allowed is between 2 to 150"),Length(min=2, max=150)])
  submit = SubmitField("Post Answer")



#Comment Section
class CommentForm(FlaskForm):
  """
  Handles Comment on answers
  """
  comment = StringField("Comment Your Answer",validators=[DataRequired(message="Enter comment between 2 and 120 characters"), Length(min=2, max=120)])
  submit = SubmitField("Post Comment")


#Create User
class CreateUserForm(FlaskForm):
  """Create User Account"""
  username = StringField("Username", validators=[DataRequired(message="Username is required"),Length(min=2, max=20)])
  password = PasswordField("Password",validators=[DataRequired(message="Password is required"),Length(min=2, max=30)])
  confirm_password = PasswordField("Confirm Password", validators=[DataRequired(message="Confirm Your Password"),Length(min=2, max=30)])
  email = StringField("Email", validators=[DataRequired(),Email()])
  submit = SubmitField("Create Account")



#User Login
class LoginForm(FlaskForm):
  """Handles User Login"""
  username = StringField("Username",validators=[DataRequired(message="Username is needed"),Length(min=2, max=20)])
  password = PasswordField("Password",validators=[DataRequired(message="Password is needed"),Length(min=2, max=30)])
  email = StringField("Email", validators=[DataRequired(message="Enter correct email"), Email()])
  submit = SubmitField("Login")