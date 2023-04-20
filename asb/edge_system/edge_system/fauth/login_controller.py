import re
from flask import Blueprint, render_template, flash, url_for, request
from flask_login import logout_user, login_user, current_user
from werkzeug.utils import redirect
from edge_system import db
from edge_system.fauth.model.users import LoginForm, UsersLogin, RegisterForm
from edge_system import login_manager

fauth = Blueprint('fauth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return UsersLogin.query.get(user_id)


@fauth.route('/users/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm() #meta={'csrf': False}
    if form.validate_on_submit():
        if UsersLogin.query.filter_by(id_employee = form.id_employee.data).first():
            flash("Employee already registered!!", 'danger')
        else:
            user = UsersLogin(
                username=form.username.data, 
                fullname=form.fullname.data, 
                pwhash=form.password.data,
                id_employee=form.id_employee.data, 
                id_role=form.id_role.data)
            
            db.session.add(user)
            db.session.commit()
            flash("Successfully registered employee!!")
        return redirect(url_for('home.home_page'))
    
    if form.errors:
        flash(form.errors, 'danger')

    return render_template('fauth/register.html', form = form)


@fauth.route('/users/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('User already authenticated')
        return redirect(url_for('home.home_page'))
    
    form = LoginForm() #meta={'csrf': False}

    if form.validate_on_submit():

        user = UsersLogin.query.filter_by(username = form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome ' + user.fullname)
            next = request.form['next']
            #if not is_safe_url(next):
            #    return abort(400)
            return redirect(next or url_for('machine.info'))
        else:
            flash('Error: Wrong password or user', 'danger')
            return redirect(url_for('fauth.login'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('fauth/login.html', form = form)

@fauth.route('/users/logout')
def logout():
    logout_user()
    flash('Closed session!!')
    return redirect(url_for('fauth.login'))