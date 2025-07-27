import sys
from PyQt5.QtWidgets import QApplication, QLabel,QPushButton,QVBoxLayout,QWidget,QFileDialog, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import QCursor
from urllib.request import urlopen
import json
import pandas as pd
import random

with urlopen("https://opentdb.com/api.php?amount=50&category=9&difficulty=easy&type=multiple") as webpage:
    data = json.loads(webpage.read().decode())
    df=pd.DataFrame(data["results"])
    print(df.columns)
    print(len(df))

j=0
i=0
def preload_data(indx):
    question = df["question"][indx]
    correct = df["correct_answer"][indx]
    wrong = df["incorrect_answers"][indx]

    formatting = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">")
    ]

    for tuple in formatting:
        question = question.replace(tuple[0], tuple[1])
        correct = correct.replace(tuple[0], tuple[1])
    for tuple in formatting:
        wrong = [char.replace(tuple[0], tuple[1]) for char in wrong]

    parameters["question"].append(question)
    parameters["correct"].append(correct)
    all_answers=wrong+[correct]
    random.shuffle(all_answers)
    parameters["answer1"].append(all_answers[0])
    parameters["answer2"].append(all_answers[1])
    parameters["answer3"].append(all_answers[2])
    parameters["answer4"].append(all_answers[3])



parameters = {
    "question":[],
    "answer1":[],
    "answer2":[],
    "answer3":[],
    "answer4":[],
    "correct":[],
    "all_answers":[],
    "index":[random.randint(0,49)]
}

widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "display": [],
    "final": []
}


app = QApplication(sys.argv)


window = QWidget()
window.setWindowTitle("Quiz Game")
window.setFixedWidth(1000)
window.move(100, 100)  # Adjust window position
window.setStyleSheet("background: #3ec9b0")


grid = QGridLayout()

def clear_widgets():
    for widget in widgets:
        if widget != "score" and widgets[widget] != []:  # Prevent clearing the score widget
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()


def show_frame1():
    clear_widgets()
    frame1()

def start_game():
    clear_widgets()
    preload_data(parameters["index"][-1])
    frame2()

def create_buttons(answer):
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        "*{"
        "border: 4px solid '#9afcc0';"
        "color: white;"
        "font-size: 30px;"
        "border-radius: 25px;"
        "padding: 20px 0;"  # Increase padding for bigger button height
        "margin-top: 10px;"  # Reduced margin-top to bring buttons closer
        "} "
        "*:hover{"
        "background: '#9afcc0';"
        "color:white;"
        "}"
    )
    button.clicked.connect(lambda x: correctornot(answer))
    button.clicked.connect(next_qs)
    return button

def correctornot(answer):
    global i
    if answer == parameters["correct"][-1]:
        increase_score()
        #parameters["index"].pop()
        #parameters["index"].append(random.randint(0,49))
        #preload_data(parameters["index"][-1])
        i=i+1
        preload_data(i)

        widgets["question"][0].setText(parameters["question"][-1])
        widgets["answer1"][0].setText(parameters["answer1"][-1])
        widgets["answer2"][0].setText(parameters["answer2"][-1])
        widgets["answer3"][0].setText(parameters["answer3"][-1])
        widgets["answer4"][0].setText(parameters["answer4"][-1])

        print("Correct answer")
    else:
        print("Wrong answer")

score=None
def increase_score():
    global j,score
    j=j+1
    score.setText(str(j))



def next_qs():
    global i
    if i < len(df):
        preload_data(i)
        clear_widgets()
        frame2()
        i = i + 1
    else:
        clear_widgets()
        frame3()
def frame1():
    image = QPixmap("logo_Copy.png")
    if image.isNull():
        print("Error: logo image not found!")  # Debugging message
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(logo)

    # Button widget
    button = QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        "*{border: 4px solid '#9afcc0';"+
        "border-radius: 20px;"+
        "font-size: 35px;"+
        "color : #1d5934;" +
        "padding: 15px 0;"+
        "margin: 150px 200px}" +
        "*:hover{background:'#9afcc0';}"
    )
    button.clicked.connect(start_game)
    widgets["button"].append(button)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)

def frame2():
    global score
    if score is None:
        score = QLabel(str(0))
        score.setAlignment(QtCore.Qt.AlignRight)
        score.setStyleSheet(
            "font-size: 35px;"
            "color: white;"
            "padding: 20px 15px;"
            "margin: 20px 20px;"
            "background: #72f760;"
            "border: 1px solid #72f760;"
            "border-radius: 40px;"
        )

        score.setFixedSize(120, 120)
        widgets["score"].append(score)
        grid.addWidget(widgets["score"][-1], 0, 0)


    question = QLabel(parameters["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        "font-family: Shanti;" +
        "font-size: 25px;" +
        "color: 'white';" +
        "padding: 75px;"
    )
    widgets["question"].append(question)


    button1 = create_buttons(parameters["answer1"][-1])
    button2 = create_buttons(parameters["answer2"][-1])
    button3 = create_buttons(parameters["answer3"][-1])
    button4 = create_buttons(parameters["answer4"][-1])

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)

    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)


def frame3():
    global j
    image = QPixmap("final_page.png")
    if image.isNull():
        print("Error: logo image not found!")  # Debugging message
    final = QLabel()
    final.setPixmap(image)
    final.setAlignment(QtCore.Qt.AlignCenter)
    final.setStyleSheet("margin-top: 100px;")
    widgets["final"].append(final)
    display=QLabel("Your Score is:"+str(j)+" Out of 50")
    display.setStyleSheet(
        "font-family: Lucinda Calligraphy;" +
        "font-size: 60px;" +
        "color: '#057851';" +
        "padding: 75px;"
    )
    display.setAlignment(QtCore.Qt.AlignCenter)
    widgets["display"].append(display)
    grid.addWidget(widgets["display"][-1],1,0,1,2)
    grid.addWidget(widgets["final"][-1], 0, 0, 1, 2)

#main
frame1()

window.setLayout(grid)

# Show window
window.show()

# Run the application loop
sys.exit(app.exec_())
