from flask import Flask,url_for,render_template,redirect,request,flash,session
from forms import AskQuestionForm,AnswerForm,CreateUserForm,CommentForm,LoginForm,VoteForm
import os
import json
from datetime import datetime

app = Flask(__name__)

app.secret_key = "student_manual_wtf_create_forms_with_flask_2026"


DATA_DIR = 'storage'
USERS_FILE = os.path.join(DATA_DIR,'users.json')
QUESTIONS_FILE  =os.path.join(DATA_DIR,'questions.json')
COMMENTS_FILE = os.path.join(DATA_DIR,'comments.json')
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

  if not os.path.exists(QUESTIONS_FILE):
    with open(QUESTIONS_FILE, 'w', encoding='utf-8') as f:
      json.dump([], f, indent=4)

  if not os.path.exists(COMMENTS_FILE):
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
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
  questions = load_json(QUESTIONS_FILE)
  for question in questions:
    if question:
      session["question_id"] = question["question_id"]

  if form_user.validate_on_submit() and 'create_user' in request.form:
    new_username = form_user.username.data.strip()

    #check if username exists
    if any(u["username"].lower() == new_username.lower() for u in users):
      flash(f"Username {new_username} already exists!")
    else:
      users.append({
        "user_id":len(users) + 1,
        "username":new_username,
        "password":form_user.password.data,
        "confirm_password":form_user.confirm_password.data,
        "email":form_user.email.data
      })
      save_json(USERS_FILE, users)
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
    session["user_id"] = user["user_id"]
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
  return redirect(url_for('create_user'))


@app.route('/question/answer/comment', methods=['GET','POST'])
def create_ans_com():
  """Handles Question|Answers|Comment"""
  form_question = AskQuestionForm()
  form_comment = CommentForm()
  form_answer = AnswerForm()
  vote_form = VoteForm()

  
  questions = load_json(QUESTIONS_FILE)
  comments = load_json(COMMENTS_FILE)
  answers = load_json(ANSWERS_FILE)
  voters = load_json(VOTING_RECORDS_FILE)

  
  #Question Section
  if form_question.validate_on_submit() and 'question_submit' in request.form:
    questions.append({
      "author_name":session["username"],
      "question_id":len(questions) + 1,
      "user_id":session["user_id"],
      "question_title":form_question.question_title.data,
      "subject_category":form_question.subject_category.data,
      "question_details":form_question.question_details.data,
      "submitted_at":datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    })
    save_json(QUESTIONS_FILE,questions)
    flash("Question added successfully to bank")
    for q in questions:
      if q:
        session["question_id"] = q["question_id"]
    return redirect(url_for('create_ans_com'))


  #Answer Section
  if form_answer.validate_on_submit() and 'answer_submit' in request.form:
    answers.append({
      "author_name":session["username"],
      "answer_id":len(answers) + 1,
      "user_id":session["user_id"],
      "question_id":session["question_id"],
      "form_answer":form_answer.answer.data,
      "submitted_at":datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    })
    save_json(ANSWERS_FILE,answers)
    flash("Answer added successfully to the bank")
    for a in answers:
      if a:
        session["answer_id"] = a["answer_id"]
    return redirect(url_for('create_ans_com'))

  #Comment Section
  if form_comment.validate_on_submit() and 'comment_submit' in request.form:
    comments.append({
      "author_name":session["username"],
      "question_id":session["question_id"],
      "answer_id":session["answer_id"],
      "user_id":session["user_id"],
      "comment_id":len(comments) + 1,
      "comment":form_comment.comment.data,
      "submitted_at":datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
    })
    save_json(COMMENTS_FILE,comments)
    flash("Comment added successfully to bank")
    for c in comments:
      if c:
        session["comment_id"] = c["comment_id"]
    return redirect(url_for('questions_feed'))

  #Voting Section
  if request.method == "POST" and "vote_type" in request.form:
    if not vote_form.validate_on_submit():
      flash("Vote form validation failed.")
      return redirect(url_for("create_ans_com"))
    
    #answer_id = request.form.get("answer_id",type=int)
    vote_type = request.form.get("vote_type")
    
    
    
    if vote_type not in ("upvote","downvote"):
      flash("Invalid Vote!")
      return redirect(url_for('create_ans_com')) 

    for ans in answers:
      session["answer_id"] = ans["answer_id"]


    
    #create new dictionary
    new_vote = {
      "author_name":session["username"],
      "answer_id":session["answer_id"],
      "voter_id":len(voters) + 1,
      "question_id":session["question_id"],
      "vote_type":vote_type,
      "user_id":session["user_id"],
      "voted_at":datetime.now().strftime("%Y-%m-%d %H:%S:%M")
    }
    voters.append(new_vote)
    save_json(VOTING_RECORDS_FILE,voters)
    flash(f"{session["username"]} voted successfully")

    return redirect(url_for('create_ans_com'))

    
  return render_template('create_ans_com.html',form_question=form_question,form_comment=form_comment,form_answer=form_answer,questions=questions,comments=comments,answers=answers,voters=voters,vote_form=vote_form)
  


@app.route('/questions_feed')
def questions_feed():
  """Handles all question"""
  questions = load_json(QUESTIONS_FILE)
  for question in questions:
    if question:
      filtered_question = [c for c in questions if c["question_title"] == question["question_title"]]
    else:
      filtered_question = questions

  return render_template('question_feed.html',filtered_question=filtered_question,questions=questions)


@app.route('/question_detail/<int:question_id>')
def question_detail(question_id):
  """Handles individual questions with
  answers,author,date of creation
  """
  questions = load_json(QUESTIONS_FILE)
  comments = load_json(COMMENTS_FILE)
  answers = load_json(ANSWERS_FILE)
  voters = load_json(VOTING_RECORDS_FILE)
  users = load_json(USERS_FILE)


  #calculate each user's total upvotes,downvotes, and score
  user_stats = {} #create empty dictionary.

  #get the user id of each user.
  for user in users:
    user_id = str(user.get("user_id"))

    #Initialization of each user's id
    user_stats[user_id] = {
      "upvotes":0,
      "downvotes":0,
      "score":0
    }

  #count votes received on answers
  for answer in answers:
    answer_id = int(answer.get("answer_id", -1))#return -1 if the key does not exixt.

    #find the author of this answer
    author_id = str(answer.get("user_id"))

    if author_id not in user_stats:
      user_stats[author_id] = {
          "upvotes":0,
          "downvotes":0,
          "score":0
        }

    #count votes beloging to this answer
    for vote in voters:
      if int(vote.get("answer_id", -1)) == answer_id:
        if vote.get("vote_type") == "upvote":
          user_stats[author_id]["upvotes"] += 1

        elif vote.get("vote_type") == "downvote":
          user_stats[author_id]["downvotes"] += 1

  #calculate each user's score
  for user_id, stats in user_stats.items():
    stats["score"] = stats["upvotes"] - stats["downvotes"]


  question = next((q for q in questions if q.get("question_id") == question_id),None)
  comment_user = next((c for c in comments if c.get("answer_id") == question_id),None)
  ans = next((a for a in answers if a["answer_id"] == question_id),None)
  voter = next((v for v in voters if v.get("answer_id") == ans["answer_id"]),None)
  user = next((u for u in users if u.get("user_id") == question["user_id"]),None)

  
  #Calculate upvote, downvote and score separately in relation to each answer
  #for answer in answers:
    #answer_id = int(answer["answer_id"])
  #upvotes = sum(1 for vote in voters if int(vote.get("answer_id", -1)) == answer_id and  vote.get("vote_type") == "upvote")
  #downvotes = sum(1 for vote in voters if int(vote.get("answer_id", -1)) == answer_id and  vote.get("vote_type") == "downvote")
  #answer["upvotes"] = upvotes
  #answer["downvotes"] = downvotes
  #answer["score"] = upvotes - downvotes


  if not question:
    return "Information about question not found",401
  elif not comment_user:
    return "Information about comment not found",402
  elif not ans:
    return "Information about answer not found",403

  elif not voter:
      return "Information about answer not found",404
    
  return render_template('question_detail.html',question=question,comment_user=comment_user,ans=ans,user=user,voter=voter,user_stats=user_stats)



@app.route('/question/fetch')
def question_fetch():
  """Handles Fetching Questions and answers calculation"""

  count = 0

  answers = load_json(ANSWERS_FILE)
  questions = load_json(QUESTIONS_FILE)

  for question in questions:
    count = sum(
      1 for answer in answers if answer["question_id"] == question["question_id"]
    )
    question["answer_count"] = count #{"answer_count":2}

  return render_template('question.html',questions=questions)
  

if __name__ == '__main__':
  app.run(debug=True)