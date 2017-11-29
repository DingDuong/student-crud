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
  excuses = db.relationship('Excuse', backref='student', lazy="dynamic", cascade="all,delete")

  def __init__(self, first_name, last_name):
    self.first_name = first_name
    self.last_name = last_name

class Excuse(db.Model):

  __tablename__ = "excuses"

  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.Text)
  student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

  def __init__(self, text, student_id):
    self.text = text
    self.student_id = student_id


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
  return render_template('students/index.html', students=Student.query.all())

@app.route('/students/new')
def new():
  return render_template('students/new.html')

@app.route('/students/<int:id>/edit')
def edit(id):
  return render_template('students/edit.html', student=Student.query.get(id))

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
  return render_template('students/show.html', student=student)

# RESTful routes for excuses

# GET /students/<int:student_id>/excuses
# POST /students/<int:student_id>/excuses
@app.route('/students/<int:student_id>/excuses', methods=["GET", "POST"])
def excuses_index(student_id):
  # if we make a POST request (when a form is submitted)
  if request.method == 'POST':
    # create an instance of an Excuse with data from the form
    # and with the value of student_id passed to the function
    new_excuse = Excuse(request.form['text'], student_id)
    # add the instance
    db.session.add(new_excuse)
    # save the instance
    db.session.commit()
    # Make a GET to excuses_index and pass in a keyword argument
    # of student_id with a value of whatever student_id was passed to the function
    return redirect(url_for('excuses_index', student_id=student_id))
  # find all of the excuses for a specific student
  student = Student.query.get(student_id)
  # show me them in a template called excuses/index.html
  return render_template('excuses/index.html', student=student)

# GET /students/<int:student_id>/excuses/new
@app.route('/students/<int:student_id>/excuses/new')
def excuses_new(student_id):
  # show me a form to make a new excuse!
  student = Student.query.get(student_id)
  return render_template('excuses/new.html', student=student)

# GET /students/<int:student_id>/excuses/<int:id>/edit
@app.route('/students/<int:student_id>/excuses/<int:id>/edit')
def excuses_edit(student_id, id):
  # go the the database and get the excuse!
  excuse = Excuse.query.get(id)
  return render_template('excuses/edit.html', excuse=excuse)


# GET /students/<int:student_id>/excuses/<int:id>
# PATCH /students/<int:student_id>/excuses/<int:id>
# DELETE /students/<int:student_id>/excuses/<int:id>
@app.route('/students/<int:student_id>/excuses/<int:id>', methods=["GET", "PATCH", "DELETE"])
def excuses_show(student_id, id):
  excuse = Excuse.query.get(id)
  if request.method == b'PATCH':
    excuse.text = request.form['text']
    db.session.add(excuse)
    db.session.commit()
    return redirect(url_for('excuses_index', student_id=student_id))
  if request.method == b'DELETE':
    db.session.delete(excuse)
    db.session.commit()
    return redirect(url_for('excuses_index', student_id=student_id))
  return render_template('excuses/show.html', excuse=excuse)

if __name__ == '__main__':
  app.run(debug=True, port=3000)









