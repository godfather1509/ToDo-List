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

# We are setting up a Flask web application and configuring it to use a SQLite database. Here's a breakdown of what each line does:
# 1. Flask Setup:

#     Flask is a micro web framework used to create web applications in Python.
#     The app = Flask(__name__) line initializes the Flask application.
#     The @app.route() decorator is used to define routes (endpoints) for the web application.

# 2. Database Configuration:

#     SQLAlchemy is used as an ORM (Object Relational Mapper) to interact with the SQLite database.
#     app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///krishna.db" sets up the SQLite database named krishna.db.
#     The db object is created as an instance of SQLAlchemy.

# 3. ToDo Model:

#     The ToDo class defines the structure of the database table using SQLAlchemy. It has the following columns:
#         Sr: Integer, Primary Key.
#         title: String, stores the title of the task.
#         desc: String, stores the description of the task.
#         date: String, stores the date associated with the task.
#         time: String, stores the time associated with the task.
#         date_created: DateTime, stores the timestamp when the task was created.

# 4. Routes and Views:

#     @app.route("/"): This route handles the home page of the application.
#         On a GET request, it fetches all tasks from the database and displays them.
#         On a POST request, it adds a new task to the database, splitting the date and time if provided.
#         If the user checks the box (check), it starts a new thread to play an audio file at a specified time.

#     @app.route("/update/<int:Sr>"): This route handles the update of an existing task.
#         It fetches the task with the given Sr (Primary Key) and allows the user to update it.
#         If the checkbox is ticked, it starts a new thread to play an audio file at a specified time.

#     @app.route("/delete/<int:Sr>"): This route deletes the task with the given Sr from the database.

#     @app.route("/name"): This route displays a specific message, "Creator of this website is Ayush Gupta", and also renders the
#       index.html template.

# 5. Audio Player:

#     player(time): This function plays an audio file (water.mp3) using the pygame library at a specified time.
#         It continuously checks the current time and compares it to the provided time.
#         If the current time matches the specified time, it plays the audio file for 10 seconds, then stops it.

# 6. Threading:

#     The code uses Python’s threading module to run the audio player in a separate thread so that the web application remains responsive.

# 7. Starting the Application:

#     if __name__ == "__main__": ensures that the Flask application runs only if the script is executed directly.
#     with app.app_context(): db.create_all() ensures that the database tables are created before the application starts.
#     app.run(debug=True, port=1500) runs the application in debug mode on port 1500.

# 8. Template and Static Files:

#     The templates for the web pages (like index.html) should be stored in a templates folder.
#     Static files like CSS, JavaScript, and images should be placed in a static folder.