"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/')
def home_rout():
    return redirect('/users')

@app.route('/users')
def users_rout():

    users = User.query.all()
    return render_template('templates/users.html', users=users)


@app.route("/users/new", methods=["POST"])
def new_user_rout():

    new_user = User(first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'])

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def user_id_rout(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('templates/user_show.html', user=user)


@app.route('/users/<int:user_id>/edit')
def user_edit_rout(user_id):

    user = User.query.get_or_404(user_id)
    return render_template('templates/user_edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user_rout(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user_rout(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
