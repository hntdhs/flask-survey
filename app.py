from crypt import methods
from http.client import responses
from re import A
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very-secretive'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey_start():
    """User selects appropriate survey, just customer satisfaction survey for the purposes of this exercise"""

    return render_template("survey_start.html", survey=survey)
    # passing survey to survey_start.html so we have access to the customer satisfaction survey over there, can't just import it there because it's an HTML file

@app.route("/begin", methods=["POST"])
def start_survey():
    """sends user to first question and sets responses to an empty list that will be filled with replies as user answers questions"""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

app.route("/answer", methods=["POST"])
def handle_question():

    #pulls user answer for question and saves it to a variable to append
    choice = request.form['answer']

    # adds user response to the session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses) == len(survey.questions)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Show current question"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    if (len(responses) != qid):
        # Prevents user from skipping ahead to questions before answering all previous questions
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    """runs when survey has been completed"""
    return render_template("completion.html")