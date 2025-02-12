from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash   # To allow us to hash a password
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    # Let user login after signing up
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the emoil of the user that was sent to us exists in the database(validation)
        user = User.query.filter_by(email=email).first()        # Query the db by the email, .first() returns the first result. There should be only one
        
        # Check if the password = the hash stored on the server
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)    # This logs the user in  || remember=False after the flask server re-starts or clears browser history
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password', category='error')
        else:
            flash('User not found', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required  # <- Checks if the user is logged in before allowing them to access this route(Logout). Logout possible if logged in already
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    # Differentiate between GET and POST
    if request.method == 'POST':
        # Get the info sent into this form using thier names in the HTML form.
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if the user with the same email already exists in the database
        user = User.query.filter_by(email=email).first()

        # Validate the data
        if user:
            flash('Email already exists', category='success')
        elif len(email) < 4:
            flash('Email is too short', category='error')
        elif len(first_name) < 2:
            flash('First name is too short', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Passwords must be greater than 7 characters', category='error')
        else:
            # Create and add user to the database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)    # Add to the db
            db.session.commit()         # Save the changes to the db
            login_user(new_user, remember=True) # Log in

            flash('Account created successfuly!', category='success')

            # Now sign in the user and redirect the user to the home page.
            return redirect(url_for('views.home'))

        # data = request.form

    else:
        pass

    return render_template('signup.html', user=current_user)


