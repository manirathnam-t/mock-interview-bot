from flask import Flask, render_template, request, redirect, session
import mysql.connector


app = Flask(__name__)
app.secret_key = "ai_interview_secret"
# 🔑 Add your OpenAI API key here

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0104",
    database="interview_bot"
)
cursor = db.cursor()

# Generate AI question
def generate_question(role, index):
    questions = {
        "AI Engineer": [
            "What is Machine Learning?",
            "Explain Overfitting vs Underfitting",
            "What is a Neural Network?",
            "What is Gradient Descent?",
            "Explain Transformers"
        ],
        "Data Scientist": [
            "What is Data Cleaning?",
            "Explain Linear Regression",
            "What is Classification?",
            "What is Clustering?",
            "Bias vs Variance?"
        ],
        "Python Developer": [
            "What are Python lists?",
            "Explain OOP in Python",
            "What is Flask?",
            "What are decorators?",
            "Exception handling in Python?"
        ],
        "Web Developer": [
            "What is HTML?",
            "What is CSS?",
            "What is JavaScript?",
            "What is REST API?",
            "Frontend vs Backend?"
        ]
    }

    return questions.get(role, questions["Python Developer"])[index]
# AI scoring function
def evaluate_answer(question, answer):
    words = len(answer.split())

    score = 0

    if words > 50:
        score += 4
    elif words > 30:
        score += 3
    elif words > 15:
        score += 2
    elif words > 5:
        score += 1

    keywords = ["because", "example", "used", "process", "means", "define"]

    for word in keywords:
        if word in answer.lower():
            score += 1

    return min(score * 2, 10)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    session["name"] = request.form["name"]
    session["email"] = request.form["email"]
    session["role"] = request.form["role"]

    session["q_index"] = 0
    session["questions"] = []
    session["answers"] = []
    session["scores"] = []

    return redirect("/question")


@app.route("/question")
def question():
    q_index = session["q_index"]

    if q_index >= 5:
        return redirect("/result")

    # Generate AI question
    question = generate_question(session["role"], q_index)

    session["current_question"] = question

    return render_template(
        "question.html",
        question=question,
        q_number=q_index + 1
    )


@app.route("/answer", methods=["POST"])
def answer():
    answer_text = request.form["answer"]
    question = session["current_question"]

    # AI score
    score = evaluate_answer(question, answer_text)

    # Save in session
    session["answers"].append(answer_text)
    session["scores"].append(score)
    session["questions"].append(question)

    # Save in MySQL
    cursor.execute(
        "INSERT INTO interviews (name, email, role, question, answer, score) VALUES (%s, %s, %s, %s, %s, %s)",
        (session["name"], session["email"], session["role"], question, answer_text, score)
    )
    db.commit()

    session["q_index"] += 1

    return redirect("/question")


@app.route("/result")
@app.route("/result")
def result():
    total_score = sum(session["scores"])

    questions = session["questions"]
    answers = session["answers"]

    qa_pairs = list(zip(questions, answers))   # ✅ create pairs in Python

    if total_score >= 40:
        feedback = "Excellent Performance 🚀"
    elif total_score >= 30:
        feedback = "Good Job 👍"
    elif total_score >= 20:
        feedback = "Average Performance 🙂"
    else:
        feedback = "Needs Improvement 📚"

    return render_template(
        "result.html",
        name=session["name"],
        role=session["role"],
        score=total_score,
        feedback=feedback,
        qa_pairs=qa_pairs
    )


if __name__ == "__main__":
    app.run(debug=True)