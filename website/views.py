from flask import Blueprint, render_template, request, redirect, jsonify
from flask.helpers import flash, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like, Follow
from .initial import db 

views = Blueprint('views', __name__)

@views.route('/') 
@views.route("/home")

def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))

@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

@views.route("/profile/<author>")
def profile(author):
    user = User.query.filter_by(id=author).first()
    follower = current_user
    hasfollow = Follow()
    if follower.is_authenticated:
        hasfollow = Follow.query.filter_by(follower_id=follower.id, followed_id=user.id).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))
    
    return render_template("userprofile.html", Blogger = user,user = current_user, hasfollow = hasfollow)

@views.route("/follow_user/<user_id>", methods=['GET'])
@login_required
def follow(user_id):
    followed = User.query.filter_by(id=id).first()
    follower = current_user
    hasfollow = Follow.query.filter_by(follower_id=follower.id, followed_id=followed.id).first()
    if not follower:
        flash('User does not exists.', category='error')
    elif hasfollow:
        db.session.delete(hasfollow)
        db.session.commit()
    else:
        hasfollow = Follow(follower_id= follower.id, followed_id=followed.id)
        db.session.add(hasfollow)
        db.session.commit()
    return redirect(url_for('views.profile', author = followed.id))