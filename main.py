from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField,SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os
from datetime import datetime


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = "123"
db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', "sqlite:///tasks_management.db")
db.init_app(app)


class TasksForm(FlaskForm):
    task = StringField(validators=[DataRequired()])
    due_date = DateField(validators=[DataRequired()])
    Add = SubmitField()


class Tasks(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(Date)


with app.app_context():
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def home():
    tasks = db.session.execute(db.select(Tasks)).scalars()
    form = TasksForm()
    if form.validate_on_submit():
        task = Tasks(
            task=form.task.data,
            date=form.due_date.data
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    year = datetime.now().year
    return render_template("index.html", form=form, tasks=tasks, year=year)


@app.route("/delete/<int:task_id>", methods=['POST','GET'])
def delete(task_id):
    task = db.get_or_404(Tasks, task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)
