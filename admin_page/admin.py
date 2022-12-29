"""
Admin page
"""
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.security import check_password_hash

from libraryapi.models import Book, User
from .forms import LoginForm

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route('/')
@login_required
def index():
    users = User.query.all()
    return render_template('index.html', title='Admin', users=users)

@admin.route('/books/')
@login_required
def books():
    users = User.query.all()
    return render_template('books.html', title='Admin', users=users)

@admin.route('/journals/')
@login_required
def journals():
    users = User.query.all()
    return render_template('journals.html', title='Admin', users=users)

@admin.route('/users/')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', title='Admin', users=users)

@admin.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            is_password_correct = check_password_hash(user.password, password)
            if is_password_correct and user.is_admin:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('admin.login')
                return redirect(next_page)
                # return redirect(url_for('admin.index'))
            elif is_password_correct and not user.is_admin:
                flash('You are registered as a User not Admin')
                return redirect(url_for('admin.login'))
            else:
                flash('Invalid password')
                return redirect(url_for('admin.login'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('admin.login'))

    return render_template('login.html', title='Admin', form=form)


@admin.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
