from flask import Blueprint, render_template, request
from .models import Foodlist
from functools import wraps
from flask import Blueprint, render_template, request, jsonify
from .models import Foodlist
from user.authentication import login_required, login_required_session

bp_food = Blueprint('food',__name__)

@bp_food.route('/mypage/foodlist', methods=["GET", "POST", "PATCH", "DELETE"])
@login_required_session
def myfoodlist(current_user):
    if request.method == "POST":
        return Foodlist().add_food_private(current_user)
    elif request.method == "PATCH":
        requested = request.get_json()
        if "isPrivate" in requested:
            return Foodlist().toggle_private_public(current_user, requested)
        else:
            pass
    elif request.method == "DELETE":
        return Foodlist().delete_food(current_user)
    else:
        user_food_list = Foodlist().get_user_list(current_user)
        return render_template("food/mypage_food.html", foods=user_food_list)

@bp_food.route('/foodlist/public', methods=["GET", "POST", "PATCH", "DELETE"])
@login_required_session
def public_foodlist(current_user):
    if request.method == "POST":
        return Foodlist().add_food_public(current_user)
    elif request.method == "PATCH":
        pass
    elif request.method == "DELETE":
        return Foodlist().delete_food(current_user)
    else:
        public_food_list = Foodlist().get_public_list()
        return render_template("food/public_food.html", foods=public_food_list, user=current_user)
