from flask import Flask, jsonify, request
from .database import notes

class Note:
    def post_notes(self, user):
        data = request.get_json()
        if user["_id"] != data["_id"]:
            return jsonify({"result":"Not authorized to use this other person's note!"}), 400

        user_notes = notes.find_one({"_id":user["_id"]})
        if not user_notes:
            note_data = {
                "_id": user["_id"],
                "note1": data["note1"],
                "note2": data["note2"],
                "note3": data["note3"],
                "note4": data["note4"],
            }
            if notes.insert_one(note_data):
                return jsonify({"result":"Your note is successfully made!"}), 200
            else:
                return jsonify({"result":"Making note has failed.."}), 400
        else:
            if notes.update_one({"_id":user["_id"]}, {"$set": {
                "note1": data["note1"],
                "note2": data["note2"],
                "note3": data["note3"],
                "note4": data["note4"]
            }}):
                return jsonify({"result":"Your note is successfully saved!"}), 200
            else:
                return jsonify({"result":"Editing note has failed.."}), 400

    def get_notes(self, user):
        user_notes = notes.find_one({"_id":user["_id"]})
        if user_notes:
            return [user_notes["note1"], user_notes["note2"], user_notes["note3"], user_notes["note4"]]
        else:
            return []

