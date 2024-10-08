import re

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError  # Correct module for IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
    @staticmethod
    def is_valid_username(username):
        # Regex pattern for the username constraints
        pattern = r'^[a-z0-9_]{3,20}$'
        return re.match(pattern, username) is not None

# Route for the home page
@app.route('/')
def home():
    msg = request.args.get('message')  # Don't pass an empty string by default
    return render_template('index.html', message=msg)

# Route to add a user (POST request)
@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    
    if not User.is_valid_username(username):
        return redirect(url_for('home', message=f"'{username}' is an invalid username! Must be 3-20 characters long and can have only lowercase letters, numbers or '_'."))

    try:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('home', message=f"User '{username}' added successfully!"))
    except IntegrityError:
        db.session.rollback()
        return redirect(url_for('home', message=f"User '{username}' already exists!"))

# Route to delete a user (POST request)
@app.route('/remove_user', methods=['POST'])
def delete_user():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    msg = ""
    if user:
        db.session.delete(user)
        db.session.commit()
        msg = f"User '{username}' removed successfully!"
    else:
        msg = f"User '{username}' not found!"
    return redirect(url_for('home', message=msg))

# Route to modify a user (POST request)
@app.route('/modify_user', methods=['POST'])
def modify_user():
    current_username = request.form['current_username']
    new_username = request.form['new_username']
    
    if not User.is_valid_username(new_username):
        return redirect(url_for('home', message=f"'{new_username}' is an invalid username! Must be 3-20 characters long and can have only lowercase letters, numbers or '_'."))
    
    user = User.query.filter_by(username=current_username).first()
    msg = ""
    if user:
        user.username = new_username
        db.session.commit()
        msg = f"User '{current_username}' updated to '{new_username}' successfully!"
    else:
        msg = f"User '{current_username}' not found!"
    return redirect(url_for('home', message=msg))

# Route to list all users
@app.route('/users')
def list_users():
    users = User.query.all()
    return '<br>'.join([f'User: {user.username}' for user in users])

# Displays list of users in JSON format
@app.route('/users_json')
def list_users_json():
    users = User.query.all()
    return jsonify([{'username': user.username} for user in users])

# Route to remove all users
@app.route('/remove_all_users', methods=['POST'])
def remove_all_users():
    try:
        # Delete all users
        db.session.query(User).delete() # user is the table name here
        db.session.commit()
        msg = "All users removed successfully!"
    except Exception as e:
        db.session.rollback()
        msg = f"Error: {str(e)}"
    
    return redirect(url_for('home', message=msg))


if __name__ == '__main__':
    app.run(debug=True)


#########################

# some related interesting reads:

# https://stackoverflow.com/questions/4201455/sqlalchemy-whats-the-difference-between-flush-and-commit

#######################
