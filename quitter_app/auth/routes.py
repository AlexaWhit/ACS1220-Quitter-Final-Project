import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_login import login_user, logout_user, login_required, current_user
from quitter_app.models import *
from quitter_app.auth.forms import SignUpForm, LoginForm

# Import app and db from events_app package so that we can run app
from quitter_app.extensions import app, db, bcrypt

auth = Blueprint("auth", __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    # TODO: Fill out this route!
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            birth_date=form.birth_date.data,
            quit_date=form.quit_date.data,
            avg_cigs=form.avg_cigs.data,
            about_me=form.about_me.data,
            # profile_pic=form.profile_pic.data,
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=True)
        next_page = request.args.get('next')
        return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    # logout_user() is a helper function from Flask-login
    logout_user()
    return redirect(url_for('main.homepage'))