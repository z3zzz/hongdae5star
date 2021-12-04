from flask import Blueprint, render_template, request
from .models import Note
from user.authentication import login_required, login_required_session

bp_note = Blueprint('note',__name__)

@bp_note.route('/mypage/note', methods=["GET", "POST"])
@login_required_session
def mynotelist(current_user):
    if request.method == "POST":
        return Note().post_notes(current_user)
    else:
        notes = Note().get_notes(current_user)
        return render_template("/note/mypage_note.html", notes=notes, user=current_user)

