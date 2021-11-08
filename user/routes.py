from flask import Blueprint, render_template, request
from .models import User, Email_list
from functools import wraps
from .authentication import login_required, login_required_session, check_if_session_exists

bp_user = Blueprint('wow',__name__)

@bp_user.route('/register',methods=["GET","POST"])
@check_if_session_exists
def register():
    if request.method == "POST":
        return User().signup()
    else:
        return render_template('user/register.html')

@bp_user.route('/login',methods=["GET","POST"])
@check_if_session_exists
def login():
    if request.method == "POST":
        return User().login()
    else:
        return render_template('user/login.html')

@bp_user.route('/email-for-alert', methods=["POST"])
def email_register():
    return Email_list().addList()

@bp_user.route('/mypage', methods=["GET"])
@login_required_session
def myhomepage(current_user):
    return render_template('user/mypage.html', user=current_user)

@bp_user.route('/logout', methods=["GET"])
def logout():
    return User().logout()
