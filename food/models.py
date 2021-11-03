from flask import Flask, jsonify, request
from .database import food_list
from datetime import datetime, timedelta, timezone
import uuid

class Foodlist:
    def get_user_list(self, user):
        user_created_list = food_list.find({"author":user['_id']}).sort("created_date",-1)
        return user_created_list

    def get_public_list(self):
        all_public_list = food_list.find({"isPrivate":False}).sort("created_date",-1)
        return all_public_list

    def add_food_private(self, user):
        koreanTime = timezone(timedelta(hours=+9), 'KT')
        time_now = datetime.now(koreanTime)
        time_string = time_now.strftime("%Y-%m-%d %H:%M")

        new_food = {
            "_id": uuid.uuid4().hex,
            "store_name": request.form['store_name'] ,
            "menu":  request.form['menu'] ,
            "location": request.form['location']  ,
            "additional_info": request.form['additional_info'] ,
            "author": user['_id'],
            "created_date": time_string,
            "isPrivate": True
        }

        if food_list.insert_one(new_food):
            return jsonify({"result":"New food added successly!"}), 200
        else:
            return jsonify({"result":"Failed to add.."}), 400

    def add_food_public(self, user):
        new_food = {
            "_id": uuid.uuid4().hex,
            "store_name": ""  ,
            "menu":  "" ,
            "location":  "" ,
            "additional_info": ""  ,
            "author": user._id,
            "created_date": time_string,
            "isPrivate": False
        }

        food_list.insert_one(new_food)

        return jsonify({"result":"New food added successly!"}), 200

    def add_opinion(self,user):
        return

    def delete_food(self, user):
        food_to_delete = food_list.find_one({"_id": request.form["food_id"]})

        if not food_to_delete:
            return jsonify({"result":"Failed to find the requested food from food list"}), 400
        if not user['_id'] == food_to_delete['author']:
            return jsonify({"result":"You are not the writer of this foodlist, not authorized!"}), 401

        if food_list.delete_one(food_to_delete):
            return jsonify({"result": "Delete succeded!"}), 200

        return jsonify({"result": "Failed to delete the food.. sorry"})






