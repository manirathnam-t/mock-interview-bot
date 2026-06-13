from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)

# =========================
# SECRET KEY (SAFE FOR CLOUD)
# =========================
app.secret_key = os.environ.get("SECRET_KEY", "ai_interview_secret")


# =========================
# DATABASE INIT (SQLite)
# =========================
def init_db():
    conn = sqlite3.connect("interview_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            role TEXT,
            question TEXT,
            answer TEXT,
            score INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()


# =========================
# QUESTION BANK
# =========================
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


# =========================
# SCORING SYSTEM
# =========================
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


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# START INTERVIEW
# =========================
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


# =========================
# QUESTION PAGE
# =========================
@app.route("/question")
def question():
    q_index = session.get("q_index", 0)

    if q_index >= 5:
        return redirect("/result")

    question_text = generate_question(session["role"], q_index)
    session["current_question"] = question_text

    return render_template(
        "question.html",
        question=question_text,
        q_number=q_index + 1
    )


# =========================
# ANSWER SUBMIT
# =========================
@app.route("/answer", methods=["POST"])
def answer():
    answer_text = request.form["answer"]
    question = session.get("current_question")

    score = evaluate_answer(question, answer_text)

    # Safe session handling
    session["answers"] = session.get("answers", []) + [answer_text]
    session["scores"] = session.get("scores", []) + [score]
    session["questions"] = session.get("questions", []) + [question]

    session["q_index"] = session.get("q_index", 0) + 1

    # Save to SQLite
    conn = sqlite3.connect("interview_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interviews (name, email, role, question, answer, score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session["name"],
        session["email"],
        session["role"],
        question,
        answer_text,
        score
    ))
    conn.commit()
    conn.close()

    return redirect("/question")


# =========================
# RESULT PAGE
# =========================
@app.route("/result")
def result():
    total_score = sum(session.get("scores", []))

    qa_pairs = list(zip(
        session.get("questions", []),
        session.get("answers", [])
    ))

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
        name=session.get("name"),
        role=session.get("role"),
        score=total_score,
        feedback=feedback,
        qa_pairs=qa_pairs
    )


# =========================
# RUN (IMPORTANT FOR RENDER)
# =========================
if __name__ == "__main__":
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)