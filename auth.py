
####################################################################
##############          Import packages      #######################
####################################################################

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db


####################################################################

auth = Blueprint('auth', __name__) # create a Blueprint object that  we name 'auth'

####################################################################


@auth.route('/login', methods=['GET', 'POST']) # define login page path
##############################################################################
# define login page fucntion
def login():
    if request.method=='GET': # if the request is a GET we return the login page
        return render_template('login.html')

###############################################################################   

# if the request is POST the we check if the user exist and with te right password
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()

#################################################################################
# check if the user actually exists take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))

##################################################################################
 # if the user doesn't exist or password is wrong, reload the page if the above check passes, then we know the user has the right credentials
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

###################################################################################

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
##################################################################
# we define the sign  up path
@auth.route('/signup', methods=['GET', 'POST'])
##################################################################
 
# define the sign up function
def signup():
####################################################################
 # If the request is GET we return the  sign up page and forms
    if request.method=='GET':
        return render_template('signup.html')

####################################################################
# if the request is POST, then we check if the email  doesn't already exist and then we save data
    else:
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
# if this returns a user, then the email already exists in database

######################################################################
# if a user is found, we want to redirect back to signup page so user can try again
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

########################################################################
# create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256')) #add the new user to the db
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

#########################pytho###########################################

@auth.route('/learn')
@login_required
def learn():
    return render_template('Learn.html')

##########################################################################

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))