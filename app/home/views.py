from flask import render_template, redirect, url_for, request, session, g
from flask_ldap3_login.forms import LDAPLoginForm
from flask_login import login_user, logout_user, current_user

from app import users, ldaplogin_manager, login_manager
from app.models import User

from . import home


@login_manager.user_loader
def load_user(uid):
    if uid in users:
        return users[uid]
    return None


@ldaplogin_manager.save_user
def save_user(dn, username, data, memberships):
    user = User(dn, username, data)
    users[dn] = user
    return user


@home.before_app_request
def before_request():
    g.user = current_user


@home.route('/')
def index():
    return render_template("index.html")


@home.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('home.index'))
    form = LDAPLoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        login_user(form.user)
        return redirect(request.args.get('next') or url_for('home.index'))
    return render_template('login.html', form=form)


@home.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    return redirect(url_for('home.index'))
