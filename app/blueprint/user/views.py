import traceback
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.blueprint.teacher.models import Teacher
from app.blueprint.user.models import User

user = Blueprint('user', __name__)


@user.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        try:
            username = data['email']
            if User.query.filter_by(username=username).all():
                error = f"User {username} is already registered."
                return jsonify(response=error, status=400)
            new_teacher = Teacher(name=data['name'], email=data['email'], department=data['department'],
                                  phoneNo=data['phone_no'])
            db.session.add(new_teacher)
            db.session.flush()
            last_id = new_teacher.id
            new_user = User(user_type=data['user_type'], user_id=last_id, username=data['email'],
                            password=generate_password_hash(data['password']))
            db.session.add(new_user)
            db.session.commit()
            return jsonify(response="Successfully Registered", status=200)
        except Exception as e:
            return jsonify(response=traceback.format_exc(), status=400)
    return jsonify(response="Register", status=200)
