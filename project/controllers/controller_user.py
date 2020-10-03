from flask import Blueprint, request, jsonify
from project import db
from project.models.userModel import UsersModel
from flask_cors import CORS
from passlib.hash import sha256_crypt

# Blueprint Config
user_bp = Blueprint("user_bp", __name__)
module = "users"
CORS(user_bp)


@user_bp.route("/users", methods=["POST"])
def signup():
    json_data = request.json["data"]
    try:
        if json_data["password"] != json_data["password2"]:
            return jsonify({"error": "Passwords dont match"}), 500

        user = UsersModel.query.filter_by(email=json_data["email"]).first()

        if user:
            return jsonify({"error": "User already exists."}), 500

        hashedPassword = sha256_crypt.encrypt(json_data["password"])

        new_user = UsersModel(
            first_name=json_data["firstName"],
            last_name=json_data["lastName"],
            email=json_data["email"],
            password=hashedPassword,
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 200
    except Exception as err:
        return jsonify({"error": f"{err}"})


@user_bp.route("/users", methods=["GET"])
def getUsers():
    pass
