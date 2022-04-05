from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps
from werkzeug.security import check_password_hash

# CONFIG
import config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.Config')
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)


def login_required(f):
    """ basic auth for api """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return jsonify(response="Authentication Required", status=401)
        else:
            users = User.query.filter_by(username=auth.username).first()
            error = None
            if users is None:
                error = 'Incorrect username.'
            elif not check_password_hash(users.password, auth.password):
                error = 'Incorrect password.'
            if error is not None:
                return jsonify(response=f"Authentication Failed {error}", status=401)
            return f(*args, **kwargs)

    return decorated_function


# BLUEPRINTS
from app.blueprint.user.views import user
from app.blueprint.teacher.views import teacher
from app.blueprint.student.views import student

app.register_blueprint(user)
app.register_blueprint(teacher)
app.register_blueprint(student)



# ROUTES
@app.route('/', methods=['GET', 'POST'])
def home():
    """homepage"""
    return "Welcome"
