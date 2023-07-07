import re
from flask import Blueprint, render_template, flash, url_for, request
from flask_login import logout_user, login_user, current_user
from werkzeug.utils import redirect
from werkzeug.security import check_password_hash, generate_password_hash
from edge_system import db, login_manager
from edge_system.fauth.model.users import LoginForm, UsersLogin, RegisterForm

fauth = Blueprint('fauth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return UsersLogin.query.get(user_id)

@fauth.route('/users/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated and current_user.id_role.value=='Administrador':

        form = RegisterForm() #meta={'csrf': False}
        if form.validate_on_submit():
            if UsersLogin.query.filter_by(id_employee = form.id_employee.data).first() and UsersLogin.query.filter_by(id = form.id.data).first():
                flash("Employee already registered!!", 'danger')
                return render_template('fauth/register.html', form = form)
            else:
                user = UsersLogin(request.form['id'],
                                request.form['username'],
                                request.form['fullname'], 
                                request.form['password'],
                                request.form['id_employee'],
                                request.form['id_role'])
                
                db.session.add(user)
                db.session.commit()
                flash("Successfully registered employee!!")
            return redirect(url_for('home.home_page'))
        
        if form.errors:
            flash(form.errors, 'danger')

        return render_template('fauth/register.html', form = form)
    
    flash('Ingresar como administrador para registrar usuario','danger')
    return redirect(url_for('fauth.login'))
    


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
            return redirect(next or url_for('home.home_page'))
        else:
            flash('Error: Wrong password or user', 'danger')
            return redirect(url_for('fauth.login'))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template('fauth/login.html', form = form)

@fauth.route('/users/show/<int:id>')
def user_show(id):
    user = UsersLogin.query.get_or_404(id)
    return render_template('fauth/show.html', user = user)
    

@fauth.route('/users/update/<int:id>', methods=['POST','GET'])
def user_update(id):

    if current_user.is_authenticated and current_user.id_role.value=='Administrador':

        user = UsersLogin.query.get_or_404(id)

        form = RegisterForm()

        if request.method == 'GET':
            form.id.data = user.id
            form.username.data = user.username
            form.fullname.data = user.fullname
            form.id_employee.data = user.id_employee
            form.id_role.data = user.id_role

        if form.validate_on_submit():
            user.id = form.id.data
            user.username = form.username.data
            user.fullname = form.fullname.data
            user.pwhash = generate_password_hash(form.password.data)
            user.id_employee = form.id_employee.data
            user.id_role = form.id_role.data

            db.session.add(user)
            db.session.commit()
            flash("Usuario actualizado con exito")
            return redirect(url_for('fauth.user_show', id=user.id))
        
        if form.errors:
            flash(form.errors,'danger')

        return render_template('fauth/update.html',user=user, form=form)
    
    flash('Ingresar como administrador','danger')
    return redirect(url_for('fauth.login'))

@fauth.route('/users/info_all')
def users_info_all():
    if current_user.is_authenticated and current_user.id_role.value=='Administrador':

        users=UsersLogin.query.all()
        print(users)
        return render_template("fauth/users_info.html", users=users)
    
    flash('Ingresar como administrador','danger')
    return redirect(url_for('fauth.login'))


@fauth.route('/users/delete/<int:id>')
def user_delete(id):
    if current_user.is_authenticated and current_user.id_role.value=='Administrador':

        user=UsersLogin.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        flash("Usuario borrado con exito")
        return redirect(url_for('fauth.users_info_all'))
    
    flash('Ingresar como administrador','danger')
    return redirect(url_for('fauth.login'))


@fauth.route('/users/logout')
def logout():
    logout_user()
    flash('Closed session!!')
    return redirect(url_for('fauth.login'))