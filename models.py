from database import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))


class Interview(db.Model):
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    role_name = db.Column(db.String(100))


class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)

    interview_id = db.Column(db.Integer)

    question_number = db.Column(db.Integer)

    question_text = db.Column(db.Text)

    speech_text = db.Column(db.Text)

    user_answer = db.Column(db.Text)

    ai_feedback = db.Column(db.Text)

    score = db.Column(db.Integer)