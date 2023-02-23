import os
import random
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import datetime
from quitter_app.auth.forms import SignUpForm
from quitter_app.models import *
from quitter_app.main.forms import ReactionForm, PostForm, UserForm
from flask_login import login_user, logout_user, login_required, current_user
from quitter_app.extensions import app, db, bcrypt


main = Blueprint("main", __name__)

##########################################
#           MAIN Routes                  #
##########################################

@main.route('/')
# COMPLETED
def homepage():
    # Print all the posts of users friends
    all_posts = Post.query.all()
    all_users = User.query.all()
    return render_template('home.html', 
        all_posts=all_posts, all_users=all_users, datetime=datetime, random=random)

@main.route('/profile/<username>')
# COMPLETED
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(created_by=user).all()
    print(len(posts))
    return render_template('profile.html', user=user, posts=posts, datetime=datetime, random=random)


@main.route('/new_post', methods=['GET', 'POST'])
# COMPLETED
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            audience=form.audience.data,
            body =form.body.data,
            photo_url=form.photo_url.data,
            created_by=current_user,
        )
        db.session.add(new_post)
        db.session.commit()

        flash(f'Success! Your post was created successfully.')
        return redirect(url_for('main.homepage'))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_post.html', form=form)

@main.route('/post/<post_id>/reaction/new', methods=['GET', 'POST'])
# NEEDS WORK
@login_required
def new_reaction(post_id):
    form = ReactionForm()

    if form.validate_on_submit():
        new_reaction = Reaction(
            reaction=form.reaction.data,
            comment=form.comment.data,
            photo_url=form.photo_url.data,
            created_by=current_user,
        )
        db.session.add(new_reaction)
        db.session.commit()

        flash(f'Success! Your reaction was created successfully.')
        return redirect(url_for('main.post_detail', post_id=post_id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_reaction.html', form=form)

@main.route('/user/<user_id>', methods=['GET', 'POST'])
# NEED TO WORK ON THE FORM
@login_required
def edit_profile(user_id):
    user = User.query.get(user_id)
    form = SignUpForm(obj=user)
 
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()

# THIS PART ISN'T LOADING ONCE THE USER CLICKS THE SUBMIT BUTTON
        flash(f'Good News! {user.username} was UPDATED successfully.')
        return redirect(url_for('main.profile', user_id=user.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('edit_profile.html', user=user, form=form, datetime=datetime, random=random)

@main.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
# COMPLETED
def edit_post(post_id):
    post = Post.query.get(post_id)
    form = PostForm(obj=post)

    # STRETCH - Add delete capability
    if form.delete.data:
        return redirect(url_for('main.delete_post', post_id=post.id)) 


    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()

        flash(f'Good News! Your post was UPDATED successfully.')
        return redirect(url_for('main.homepage'))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('edit_post.html', post=post, form=form)

@main.route('/delete/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_account(post_id):
    post = Post.query.get(post_id)
    # Stretch - delete the item
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Successfully deleted {} post'.format(post))
        return redirect(url_for('main.homepage'))
    finally:
        flash(' ')

@main.route('/delete/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    # Stretch - delete the item
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Successfully deleted {} post'.format(post))
        return redirect(url_for('main.homepage'))
    finally:
        flash(' ')
@main.route('/delete/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_reaction(post_id):
    post = Post.query.get(post_id)
    # Stretch - delete the item
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Successfully deleted {} post'.format(post))
        return redirect(url_for('main.homepage'))
    finally:
        flash(' ')
