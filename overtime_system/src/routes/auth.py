from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from ..models.user import User
from .. import db # Assuming db is initialized in src/__init__.py or src/main.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

auth_bp = Blueprint('auth', __name__)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index')) # Assuming a main blueprint with an index route
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Login bem-sucedido!', 'success')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Login sem sucesso. Verifique o email e a senha.', 'danger')
    return render_template('login.html', title='Login', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))

# Placeholder for user registration - to be implemented if needed for collaborators by admin
# For now, admin user (overtimecap@gmail.com) will be created manually or via a script.

