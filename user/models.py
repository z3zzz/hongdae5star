from flask import Flask, jsonify, request
from .database import user_info, email_list
import uuid
from datetime import datetime, timedelta, timezone
from passlib.hash import pbkdf2_sha256
from .authentication import provide_jwt, create_session, remove_session

class User:
    def signup(self):
        koreanTime = timezone(timedelta(hours=+9), 'KT')
        time_now = datetime.now(koreanTime)
        time_string = time_now.strftime("%Y-%m-%d %H:%M")

        user = {
            "_id": uuid.uuid4().hex,
            "user_id": request.form['user_id'],
            "user_pw": request.form['user_pw'],
            "user_nickname": request.form['user_nickname'],
            "favorite_food": request.form['favorite_food'],
            "register_date": time_string
        }
        user['user_pw'] = pbkdf2_sha256.encrypt(user['user_pw'])

        if user_info.find_one({"user_id":request.form['user_id']}):
           return jsonify({"error":"This id is already in use.. Please try another one!"}), 400

        if user_info.insert_one(user):
           return jsonify(user), 200

        return jsonify({"error": "Signup failed.."}), 400

    def login(self):
        user = {
            "user_id": request.form['user_id'],
            "user_pw": request.form['user_pw'],
            }

        if not user_info.find_one({"user_id":user['user_id']}):
            return jsonify({"error":"Please check again your id.."}), 400

        userInDatabase = user_info.find_one({"user_id":user['user_id']})

        if not pbkdf2_sha256.verify(user['user_pw'], userInDatabase['user_pw']):
            return jsonify({"error": "Please check again your password.."}), 400

        #return provide_jwt(userInDatabase)
        return create_session(userInDatabase)

    def logout(self):
        return remove_session()

class Email_list:
    def addList(self):
        koreanTime = timezone(timedelta(hours=+9), 'KT')
        time_now = datetime.now(koreanTime)
        time_string = time_now.strftime("%Y-%m-%d %H:%M")

        current_count = email_list.count_documents({})
        email = {"_id":current_count + 1,
                 "email":request.form['email_address'],
                 "added_date": time_string
                }
        if email_list.find_one({"email":email["email"]}):
            return jsonify({"result":"email already in the list"})

        if email_list.insert_one(email):
            return jsonify({"result":"success"})

        return jsonify({"result":"fail"})
