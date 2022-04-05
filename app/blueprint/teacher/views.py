import traceback
from flask import Blueprint, request, jsonify, Response
from app import db, login_required
from app.blueprint.student.models import Student

teacher = Blueprint('teacher', __name__)


@teacher.route('/student', methods=['POST', 'GET'])
@login_required
def add_student():
    """This function will allow teachers to add each student"""
    try:
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
                for stud in data.get('students'):
                    new_stud = Student(name=stud.get('name'), std=stud.get('std'), dob=stud.get('dob'))
                    db.session.add(new_stud)
                db.session.commit()
                message = "Students has been added successfully."
                return jsonify(response=message, status=200)
            else:
                message = "The request payload is not in JSON format"
                return jsonify(response=message, status=400)
        elif request.method == "GET":
            students = Student.query.all()
            dict_count = {}
            for count, data in enumerate(students):
                stud = {}
                for column in data.__table__.columns:
                    stud[column.name] = str(getattr(data, column.name))
                    dict_count[count] = stud
            return jsonify(response=dict, status=200)
    except Exception as e:
        return jsonify(response=traceback.format_exc(), status=400)


@teacher.route('/bulk_upload', methods=['POST', 'GET'])
@login_required
def upload_csv():
    """This function will read a csv file and upload the data to database"""
    try:
        file = request.files['file']
        if file:
            f = file.read()
            csv_data = f.decode("utf-8")
            splits = csv_data.split('\n')
            for stud in splits:
                students = stud.split(',')
                if len(students) > 1:
                    new_stud = Student(name=students[0], std=students[1], dob=students[2])
                    db.session.add(new_stud)
            db.session.commit()
            return jsonify(response="Students added successfully", status=200)
        return jsonify(response="File not found", status=400)
    except Exception as e:
        return jsonify(response=traceback.format_exc(), status=400)
