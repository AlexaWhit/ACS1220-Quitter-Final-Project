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
    return render_template('profile.html', user=user, datetime=datetime, random=random)


@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            audience=form.audience.data,
            body =form.body.data,
            photo_url=form.photo_url.data,
        )
        db.session.add(new_post)
        db.session.commit()

        flash('Success! The new POST was created successfully.')
        return redirect(url_for('main.post_detail', post_id=new_post.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_post.html', form=form)

@main.route('/user/<user_id>', methods=['GET', 'POST'])
# NEED TO WORK ON THE FORM
@login_required
def user_detail(user_id):
    user = User.query.get(user_id)
    form = SignUpForm(obj=user)
 
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()

# THIS PART ISN'T LOADING ONCE THE USER CLICKS THE SUBMIT BUTTON
        flash(f'Good News! {user.username} was UPDATED successfully.')
        return redirect(url_for('main.profile', username=user.username))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('user_detail.html', user=user, form=form, datetime=datetime, random=random)

@main.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = Post.query.get(post_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    form = PostForm(obj=post)

    # STRETCH - Add delete capability
    if form.delete.data:
        return redirect(url_for('main.delete_post', post_id=post.id)) 

    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()

        flash('Good News! The post was UPDATED successfully.')
        return redirect(url_for('main.post_detail', post_id=post.id))

    # TODO: Send the form to the template and use it to render the form fields
    return render_template('post_detail.html', post=post, form=form)

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
