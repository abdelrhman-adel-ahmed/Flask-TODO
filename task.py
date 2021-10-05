from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__, template_folder="templates")

# /// relative path //// absoulte path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f"Task {self.id}"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        if not task_content:
            return "there was an isuue"

        new_task = ToDo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "there was an isuue"
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template("main/index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "there was an isuue"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task_to_update = ToDo.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "there was an isuue"
    else:
        return render_template("main/update.html", task=task_to_update)


if __name__ == "__main__":
    app.run(debug=True)
