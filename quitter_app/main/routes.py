import os
from pdb import post_mortem
import random
from urllib import response
from flask import abort, Blueprint, request, render_template, redirect, url_for, flash
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
    reactions = Reaction.query.all()
    return render_template('home.html', 
        all_posts=all_posts, all_users=all_users, reactions=reactions, datetime=datetime, random=random)

@main.route('/profile/<username>')
# COMPLETED
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(created_by=user).all()
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


    return render_template('new_post.html', form=form)

@main.route('/post/<post_id>/reaction/add', methods=['GET', 'POST'])
@login_required
# COMPLETED
def add_reaction(post_id):
    post = Post.query.get(post_id)
    form = ReactionForm(request.form)

    if form.validate_on_submit():
        new_reaction = Reaction(
            reaction=form.reaction.data,
            comment=form.comment.data,
            created_by=current_user,
            post=post
        )
        db.session.add(new_reaction)
        db.session.commit()

        flash(f'Success! Your reaction was created successfully.')
        return redirect(url_for('main.homepage'))

    return render_template('add_reaction.html', form=form, post=post)

@main.route('/user/<user_id>', methods=['GET', 'POST'])
@login_required
# COMPLETED
def edit_profile(user_id):
    user = User.query.get(user_id)
    form = UserForm(obj=user)
 
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()

        flash(f'Good News! {user.username} was UPDATED successfully.')
        return redirect(url_for('main.user_profile', username=current_user.username))

    return render_template('edit_profile.html', user=user, form=form, datetime=datetime, random=random)

@main.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
# COMPLETED
def edit_post(post_id):
    post = Post.query.get(post_id)
    if post.created_by != current_user:
        abort(403)
    form = PostForm(obj=post)

    if form.delete.data:
        return redirect(url_for('main.delete_post', post_id=post.id)) 

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.add(post)
        db.session.commit()

        flash(f'Good News! Your post was UPDATED successfully.')
        return redirect(url_for('main.homepage'))

    return render_template('edit_post.html', post=post, form=form)

@main.route('/post/<int:post_id>/reaction/<int:reaction_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_reaction(post_id, reaction_id):
    reaction = Reaction.query.get_or_404(reaction_id)
    post = reaction.post
    if reaction.created_by != current_user:
        abort(403)
    form = ReactionForm(obj=reaction)

    if form.delete.data:
        return redirect(url_for('main.delete_reaction', reaction_id=reaction.id)) 

    if form.validate_on_submit():
        form.populate_obj(reaction)
        db.session.add(reaction)
        db.session.commit()

        flash(f'Good News! Your reaction was UPDATED successfully.')
        return redirect(url_for('main.homepage'))

    elif request.method == 'GET':
        form.comment.data = reaction.comment

    if reaction is None:
        flash('Reaction does not exist.')
        return redirect(url_for('main.homepage'))

    return render_template('edit_reaction.html', title='Edit Reaction', form=form, post=post, reaction=reaction)

@main.route('/delete/<post_id>', methods=['GET', 'POST'])
#COMPLETED
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)

    try:
        db.session.delete(post)
        db.session.commit()
        flash('Successfully deleted {} post'.format(post))
        return redirect(url_for('main.homepage'))
    finally:
        flash(' ')

@main.route('/delete/<reaction_id>', methods=['POST'])
@login_required
def delete_reaction(reaction_id):
    reaction = Reaction.query.get_or_404(reaction_id)

    if reaction.created_by != current_user:
        abort(403)

    try:
        db.session.delete(reaction)
        print("Reaction deleted successfully!")
        db.session.commit()
        flash('Successfully deleted reaction.')
    except:
        db.session.rollback()
        flash('Could not delete reaction.')
    
    return redirect(url_for('main.homepage'))


@main.route('/add_friend/<username>', methods=['GET', 'POST'])
@login_required
def add_friend(username):
    new_friend = User.query.filter_by(username=username).first()

    if new_friend not in current_user.friend_list and new_friend is not None:
        current_user.friend_list.append(new_friend)
        db.session.commit()
        flash(f'Success! {new_friend.username} has been ADDED to your friend list!')  
        return redirect(url_for('main.user_profile', username=new_friend.username)) 
    else:   
        return (f"Aw shucks! {new_friend.username} is already in your friend list :)")

@main.route('/remove_friend/<username>', methods=['POST'])
@login_required
def remove_friend(username):
    user = User.query.filter_by(username=username).first()

    if user in current_user.friend_list:
        current_user.friend_list.remove(user)
        db.session.commit()
        flash(f'Success! {user.username} has been REMOVED from your friend list!')   
        return redirect(url_for('main.user_profile', username=user.username)) 
    else:   
        return "ERROR!"