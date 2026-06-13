from openai import OpenAI
from config import OPENAI_API_KEY
import random
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_question(role):

    questions = {
        "AI Engineer": [
            "What is Machine Learning?",
            "What is Deep Learning?",
            "What is the difference between supervised and unsupervised learning?",
            "What is overfitting and how can it be prevented?",
            "What is a neural network?"
        ],

        "Data Scientist": [
            "What is data preprocessing?",
            "What is feature engineering?",
            "What is the difference between correlation and causation?",
            "What is cross validation?",
            "Explain the bias-variance tradeoff."
        ],

        "Python Developer": [
            "What are Python decorators?",
            "What is the difference between a list and a tuple?",
            "Explain OOP concepts in Python.",
            "What is exception handling?",
            "What are generators in Python?"
        ],

        "Web Developer": [
            "What is the difference between GET and POST?",
            "What is REST API?",
            "What is the purpose of JavaScript?",
            "What is responsive web design?",
            "Explain session and cookies."
        ]
    }

    return random.choice(
        questions.get(role, ["Tell me about yourself."])
    )
def evaluate_answer(question, answer):

    answer = answer.lower()

    if len(answer) > 100:
        return {
            "score": 9,
            "status": "Suitable",
            "feedback": "Excellent answer with sufficient explanation."
        }

    elif len(answer) > 40:
        return {
            "score": 6,
            "status": "Partially Suitable",
            "feedback": "Good attempt, but more details are needed."
        }

    else:
        return {
            "score": 3,
            "status": "Not Suitable",
            "feedback": "Answer is too short and lacks explanation."
        }