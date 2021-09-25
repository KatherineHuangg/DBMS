# export FLASK_ENV=development
# export FLASK_APP=run
# flask run --port 8000


from collections import namedtuple
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify, send_from_directory
from flask import request
from flask_cors import CORS
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy(app)
# db.init_app(app)

class Doctor(db.Model):
    __tablename__ = 'doctor'
    dnum = db.Column(db.Integer, primary_key=True)
    did = db.Column(db.String(10), nullable=True)
    sex = db.Column(db.String(2), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    dno = db.Column(db.Integer, db.ForeignKey('department.dno'), nullable=False)

    db_doctor_look = db.relationship("Look", backref="doctor")

class Nurse(db.Model):
    __tablename__ = 'nurse'
    nnum = db.Column(db.Integer, primary_key=True)
    nid = db.Column(db.String(10), nullable=True)
    sex = db.Column(db.String(2), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)

    db_nurse_look = db.relationship("Look", backref="nurse")

class Patient(db.Model):
    __tablename__ = 'patient'
    pid = db.Column(db.String(10), primary_key=True)
    sex = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    dno = db.Column(db.Integer, db.ForeignKey('department.dno'), nullable=False)
    cases = db.Column(db.Integer, db.ForeignKey('register.cases'), nullable=False)

    db_patient_money = db.relationship("Money", backref="patient")
    db_patient_look = db.relationship("Look", backref="patient")
    # db_patient_register = db.relationship("Register", backref="patient")


class DeskStaff(db.Model):
    __tablename__ = 'deskstaff'
    sid = db.Column(db.String(10), primary_key=True)
    sex = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(20), nullable=False)

    db_deskstaff_register = db.relationship("Register", backref="deskstaff")

class Look(db.Model): #看診
    __tablename__ = 'look'
    cases = db.Column(db.Integer, primary_key=True)
    # cases = db.Column(db.Integer, db.ForeignKey('register.cases'), nullable=False)
    pid = db.Column(db.String(10), db.ForeignKey('patient.pid'), nullable=False)
    did = db.Column(db.String(10), db.ForeignKey('doctor.did'), nullable=False)
    nid = db.Column(db.String(10), db.ForeignKey('nurse.nid'), nullable=False)

class Department(db.Model):
    __tablename__ = 'department'
    dname = db.Column(db.String(20), nullable=False)
    dno = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(5), nullable=False)

    db_depart_doctor = db.relationship("Doctor", backref="department")
    db_depart_patient = db.relationship("Patient", backref="department")


class Register(db.Model):
    __tablename__ = 'register'
    cases = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.String(10), db.ForeignKey('deskstaff.sid'), nullable=False)
    pid = db.Column(db.String(10), nullable=False)

    # db_register_money = db.relationship("Money", backref="register")
    # db_register_look = db.relationship("LOok", backref="register")
    db_register_patient = db.relationship("Patient", backref="register")

class Money(db.Model):
    __tablename__ = 'money'
    cases = db.Column(db.Integer, primary_key=True)
    # cases = db.Column(db.Integer, db.ForeignKey('register.cases'), nullable=False)
    pid = db.Column(db.String(10), db.ForeignKey('patient.pid'), nullable=False)
    staffname = db.Column(db.String(20), nullable=False)
    paymoney = db.Column(db.String(20), nullable=False)

@app.route('/create_db')
def index():
    db.create_all()
    return 'ok'

#get word count
@app.route('/query',methods=['GET','POST'])
def wordcount():
    query = request.values.get('query')
    # print(query)
    # return "ok"
    query_data = db.engine.execute(query).fetchall()
    return json.dumps([dict(r) for r in query_data])


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)