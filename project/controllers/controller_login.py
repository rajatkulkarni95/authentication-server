from flask import Blueprint, request, jsonify
from flask import current_app
from os import getenv
from datetime import timedelta
from project.models.userModel import UsersModel
from flask_cors import CORS
from passlib.hash import sha256_crypt
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)

# Blueprint Config
login_bp = Blueprint("login_bp", __name__)
module = "login"
CORS(login_bp)

# JWT Setup
current_app.config["JWT_SECRET_KEY"] = getenv("JWT_SECRET_KEY")
jwt = JWTManager(current_app)

# JWT User Model


class UserObject:
    def __init__(self, email):
        self.email = email


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {"email": user.email}


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


@login_bp.route("/login", methods=["POST"])
def login():
    json_data = request.json["data"]
    try:
        db_user = UsersModel.query.filter_by(email=json_data["email"]).first()

        if db_user is None:
            raise ValueError('User does not exist')

        if sha256_crypt.verify(json_data["password"], db_user.password):
            user = UserObject(email=db_user.email)
            expires = timedelta(days=1)

            access_token = create_access_token(
                identity=user, expires_delta=expires)
            response = {"access_token": access_token,
                        "name": db_user.first_name}

            return jsonify(response), 200
        else:
            return jsonify({"error": "Username or Password incorrect"}), 401
    except Exception as err:
        return jsonify({"error": f"{err}"}), 500
