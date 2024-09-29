from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime, threading
import time as tm
import pygame

pygame.init()
pygame.mixer.init()


def player(time):
    print("executing player function")
    while True:
        currentTime = datetime.datetime.now().strftime("%H:%M")
        if currentTime == time:
            pygame.mixer.music.load("water.mp3")
            pygame.mixer.music.play(start=20)
            t = tm.time()
            while (tm.time() - t) < 10:
                pass
            print("time hogaya")
            pygame.mixer.music.stop()
            break


app = Flask(__name__)
# creating Flask object
app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///krishna.db"
# defining sqlite database

db = SQLAlchemy(app)
# instance of SQLAlchemy used to access and modify database

class ToDo(db.Model):
    # here db.Model is the base class provided to ToDo class 
    Sr = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    checkbox=db.Column(db.String(10),nullable=False,default='off')
    # nullable means if the value here can be null or not
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sr}-{self.title}"
    # __repr__ function is used to print official string representation of object 
    # this official reresentation should ideally be able to re create our original object 


@app.route("/", methods=["GET", "POST"])
# route means endpoints if the endpoint of url is '/' then hello_world() function will run
def hello_world():
    if request.method == "POST":
        title = request.form["title"]
        # this is the special dictionary like object in Flask which holds data send by the user as value to the provided key
        # e.g. for "title" key name of task shall be the value 
        desc = request.form["desc"]
        date = request.form["time"]
        check = request.form.get("tick")
        if len(date) > 1:
            date, time = date.split(" ")
            if check:
                try:
                    t1 = threading.Thread(target=player, args=(time))
                    t1.start()
                except Exception as e:
                    print(e)
        else:
            date = datetime.date.today().strftime("%d/%m/%Y")
            time = datetime.datetime.now().strftime("%H:%M")

        todo = ToDo(title=title, desc=desc, date=date, time=time,checkbox=check)
        db.session.add(todo)
        db.session.commit()
    alltodo = ToDo.query.all()
    return render_template("index.html", alltodos=alltodo)


@app.route("/update/<int:Sr>", methods=["GET", "POST"])
def update(Sr):
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        date = request.form["time"]
        check = request.form.get("tick")
        if len(date) > 1:
            date, time = date.split(" ")
            if check:
                try:
                    t1 = threading.Thread(target=player, args=(time,))
                    t1.start()
                except Exception as e:
                    print(e)
        else:
            date = datetime.date.today().strftime("%d/%m/%Y")
            time = datetime.datetime.now().strftime("%H:%M")

        todo = ToDo.query.filter_by(Sr=Sr).first()
        todo.title = title
        todo.desc = desc
        todo.date = date
        todo.time = time
        todo.check = check
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        # if user has submitted the form html file sends "POST" request and this if condition get triggered 

    todo = ToDo.query.filter_by(Sr=Sr).first()
    # here we are searching for provided Sr. value with Sr. value in database and returns the first match if no matches than it return none
    # if no request is sent it means user is merely visting the update page
    return render_template("update.html", alltodos=todo)


@app.route("/delete/<int:Sr>", methods=["GET", "POST"])
def delete(Sr):
    alltodo = ToDo.query.filter_by(Sr=Sr).first()
    db.session.delete(alltodo)
    db.session.commit()
    return redirect("/")


@app.route("/about")
def display():
    return backgroundRender()
def backgroundRender():
    return render_template("about.html")


# make template folder to store html files
# static folder is used to store staic files(CSS,JS,Images etc.) that we want to serve as they are

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=1500)
