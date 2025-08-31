from flask import Flask, render_template, request, redirect, url_for, session
from quiz import Quiz, Question
 
import random

app = Flask(__name__)
app.secret_key = "test_environment"


quiz = Quiz()
quiz.add_question(Question("Who is the fastest runner?", ["Yohan Blake", "Asafa Powell", "Usain Bolt"], 2))
quiz.add_question(Question("Ghana was first called?", ["Salaga", "Gold Coast", "Shinning Coast"], 1))
quiz.add_question(Question("What is 2 + 2?", ["3", "4", "5"], 1))
quiz.add_question(Question("What is the capital of France?", ["London", "Paris", "Berlin"], 1))
quiz.add_question(Question("Which planet is known as the Red Planet?", ["Venus", "Mars", "Jupiter"], 1))
quiz.add_question(Question("Who painted the Mona Lisa?", ["Leonardo da Vinci", "Pablo Picasso", "Vincent van Gogh"], 0))
quiz.add_question(Question("What is the largest ocean on Earth?", ["Atlantic Ocean", "Indian Ocean", "Pacific Ocean"], 2))
quiz.add_question(Question("In which year did the Titanic sink?", ["1912", "1920", "1898"], 0))
quiz.add_question(Question("Which country is famous for the Great Wall?", ["India", "China", "Japan"], 1))
quiz.add_question(Question("Who wrote 'Romeo and Juliet'?", ["William Shakespeare", "Charles Dickens", "Jane Austen"], 0))
quiz.add_question(Question("What is the chemical symbol for gold?", ["Ag", "Au", "Gd"], 1))
quiz.add_question(Question("Which continent is the Sahara Desert located in?", ["Asia", "Africa", "Australia"], 1))
quiz.add_question(Question("What is the tallest mountain in the world?", ["K2", "Mount Everest", "Kilimanjaro"], 1))
quiz.add_question(Question("Which animal is known as the King of the Jungle?", ["Tiger", "Lion", "Elephant"], 1))
quiz.add_question(Question("How many players are there in a football (soccer) team on the field?", ["9", "10", "11"], 2))
quiz.add_question(Question("What is the boiling point of water at sea level?", ["90°C", "100°C", "120°C"], 1))
quiz.add_question(Question("Who was the first man to walk on the Moon?", ["Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin"], 0))
quiz.add_question(Question("Which is the smallest country in the world?", ["Vatican City", "Monaco", "Malta"], 0))
quiz.add_question(Question("Which language has the most native speakers?", ["English", "Mandarin Chinese", "Spanish"], 1))
quiz.add_question(Question("What is the national currency of Japan?", ["Yuan", "Yen", "Won"], 1))
quiz.add_question(Question("Which organ in the human body pumps blood?", ["Liver", "Lungs", "Heart"], 2))
quiz.add_question(Question("Which country hosted the 2016 Summer Olympics?", ["China", "Brazil", "Russia"], 1))
quiz.add_question(Question("What gas do humans need to breathe to survive?", ["Carbon Dioxide", "Oxygen", "Nitrogen"], 1))
quiz.add_question(Question("Which symbol is used to write comments in Python?", ["//", "#", "/* */"], 1))
quiz.add_question(Question("Which data type is used to store True or False values in Python?", ["int", "bool", "str"], 1))
quiz.add_question(Question("Which of these is a loop in Python?", ["for", "if", "print"], 0))
quiz.add_question(Question("What is the correct file extension for Python files?", [".py", ".java", ".cpp"], 0))
quiz.add_question(Question("Which function is used to display output in Python?", ["print()", "echo()", "show()"], 0))
quiz.add_question(Question("Which keyword is used to define a function in Python?", ["function", "def", "fun"], 1))
quiz.add_question(Question("What symbol is used for multiplication in Python?", ["*", "x", "%"], 0))
quiz.add_question(Question("Which of these is used to create a list in Python?", ["{}", "[]", "()"], 1))
quiz.add_question(Question("What is the index of the first element in a Python list?", ["0", "1", "-1"], 0))



@app.route("/")
def index():
    session["current_question"] = 0
    session["score"] = 0

    # randomly pick 20 questions from all
    selected = random.sample(range(len(quiz.questions)), 20)
    session["selected"] = selected

    return redirect(url_for("quiz_view"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz_view():
    current_question_index = session.get("current_question", 0)
    selected = session.get("selected", [])

    # stop after 20
    if current_question_index >= len(selected):
        return redirect(url_for("results"))

    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option is not None:
            question_index = selected[current_question_index]
            correct_option = quiz.questions[question_index].correct_option
            if int(selected_option) == correct_option:
                session["score"] += 1
        session["current_question"] += 1

        if session["current_question"] >= len(selected):
            return redirect(url_for("results"))

    if session["current_question"] < len(selected):
        question_index = selected[session["current_question"]]
        question = quiz.questions[question_index]
        return render_template(
            "quiz.html",
            question=question,
            question_index=session["current_question"] + 1,
            total_questions=len(selected)
        )


@app.route("/results")
def results():
    score = session.get("score", 0)
    total = len(session.get("selected", []))
    return render_template("results.html", score=score, total=total)


if __name__ == "__main__":
    app.run(debug=True)
