from flask import Blueprint, render_template, request
#from .models import Foodlist
from functools import wraps
from user.authentication import login_required, login_required_session

bp_note = Blueprint('note',__name__)

@bp_note.route('/mypage/note', methods=["GET", "POST", "PATCH"])
@login_required_session
def mynotelist(current_user):
    if request.method == "POST":
        pass
    elif request.method == "PATCH":
        pass
    else:
        return render_template("/note/mypage_note.html")

