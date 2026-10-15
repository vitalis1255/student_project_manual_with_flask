from flask import Flask,url_for,render_template,redirect,request,flash,session
from forms import AskQuestionForm,AnswerForm,CreateUserForm,CommentForm,LoginForm
import os
import json
from datetime import datetime

app = Flask(__name__)

app.secret_key = "student_manual_wtf_create_forms_with_flask_2026"


DATA_DIR = 'storage'
USERS_FILE = os.path.join(DATA_DIR,'users.json')
QUESTION_FILE  =os.path.join(DATA_DIR,'questions.json')
COMMENT_FILE = os.path.join(DATA_DIR,'comments.json')
ANSWERS_FILE = os.path.join(DATA_DIR,'answers.json')
VOTING_RECORDS_FILE = os.path.join(DATA_DIR,'votings.json')

def storage_db():
  """Handles Database Section"""
  os.makedirs(DATA_DIR, exist_ok=True)

  if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
      json.dump([
        {
          "username":"user",
          "password":"user"
        }
      ], f, indent=4)

  if not os.path.exists(QUESTION_FILE):
    with open(QUESTION_FILE, 'w', encoding='utf-8') as f:
      json.dump([], f, indent=4)

  if not os.path.exists(COMMENT_FILE):
    with open(COMMENT_FILE, 'w', encoding='utf-8') as f:
      json.dump([], f, indent=4)

  if not os.path.exists(ANSWERS_FILE):
    with open(ANSWERS_FILE, 'w', encoding='utf-8') as f:
      json.dump([], f, indent=4)

  if not os.path.exists(VOTING_RECORDS_FILE):
    with open(VOTING_RECORDS_FILE, 'w', encoding='utf-8') as f:
      json.dump([], f, indent=4)

storage_db()


def load_json(filepath):
  with open(filepath, 'r', encoding='utf-8') as f:
    return json.load(f)

def save_json(filepath, data):
  with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)


@app.route("/")
def index():
  """Redirect to create account"""
  return redirect(url_for('create_user'))


@app.route('/create_user', methods=['GET','POST'])
def create_user():
  """Handles create account by user"""

  #Get the create user form
  form_user = CreateUserForm()

  #load users
  users = load_json(USERS_FILE)

  if form_user.validate_on_submit() and 'create_user' in request.form:
    new_username = form_user.username.data.strip()

    #check if username exists
    if any(u["username"].lower() == new_username.lower() for u in users):
      flash(f"Username {new_username} already exists!")
    else:
      users.append({
        "id":1,
        "username":new_username,
        "password":form_user.password.data,
        "confirm_password":form_user.confirm_password.data,
        "email":form_user.email.data
      })
      save_json(USERS_FILE,users)
      flash(f"Account Created Successfully for {new_username}!")
      return redirect(url_for('create_user'))
  return render_template('create_user.html',form_user=form_user,users=users)



@app.route('/login/user', methods=['GET','POST'])
def login():
  """User Login Page"""

  #Get user login form
  form = LoginForm()
  if form.validate_on_submit():
    username = form.username.data.strip()
    password = form.password.data.strip()

    #load users file
    users = load_json(USERS_FILE)

    #check if username and password exist in the  users file
    user = next((u for u in users if u["username"].lower() == username.lower() and u["password"] == password), None)

    if not user:
      flash(
        f"Account for {username} or {password} does not exist. Go and create an account or check your spellings"
      )
      return redirect(url_for("login"))
    session["username"] = user["username"]
    session["password"] = user["password"]
    flash(f"Login Successful {user["username"]}!")
    return redirect(url_for('create_ans_com'))
  return render_template('login.html', form=form)    



@app.route('/logout')
def logout():
  """Logout User Page"""
  session.clear()
  flash(
    "You have been logged out successfully"
  )
  return redirect(url_for('login'))


@app.route('/question/answer/comment', methods=['GET','POST'])
def create_ans_com():
  """Handles Question|Answers|Comment"""
  if session.get('username') != 'username':
    return redirect(url_for('login'))
  


  return render_template('create_ans_com.html')
  


@app.route('/question/<int:question_id>')
def question_detail(question_id):
  """Handles individual questions with
  answers,author,date of creation
  """

  return render_template('question_detail.html')


@app.route('/questions_feed')
def questions_feed():
  """Handles all question"""

  return render_template('question_feed.html')



if __name__ == '__main__':
  app.run(debug=True)