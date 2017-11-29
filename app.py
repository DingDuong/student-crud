from flask import Flask, request, render_template, url_for, redirect
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/student-crud-in-class'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
modus = Modus(app)
db = SQLAlchemy(app)

class Student(db.Model):

  __tablename__ = "students"

  # Columns!
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.Text)
  last_name = db.Column(db.Text)

  def __init__(self, first_name, last_name):
    self.first_name = first_name
    self.last_name = last_name

@app.route('/')
def root():
  return redirect(url_for('index'))

@app.route('/students', methods=["GET", "POST"])
def index():
  if request.method == 'POST':
    new_student = Student(request.form['first_name'], request.form['last_name'])
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('index.html', students=Student.query.all())

@app.route('/students/new')
def new():
  return render_template('new.html')

@app.route('/students/<int:id>/edit')
def edit(id):
  return render_template('edit.html', student=Student.query.get(id))

@app.route('/students/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
  student = Student.query.get(id)
  if request.method == b'PATCH':
    student.first_name = request.form['first_name']
    student.last_name = request.form['last_name']
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('index'))
  if request.method == b'DELETE':
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))
  return render_template('show.html', student=student)


if __name__ == '__main__':
  app.run(debug=True, port=3000)









