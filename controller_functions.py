from flask import render_template, redirect, request, session, flash
from sqlalchemy.sql import desc
from config import db, bcrypt, EMAIL_REGEX, PASSWORD_REGEX
from models import User, Quote
def default():
    users = User.query.all()
    return render_template('index.html', users=users)
def register():
    is_valid = True
    if len(request.form['first_name']) < 1:
        is_valid = False
        flash("Please enter a first name")
    if len(request.form['last_name']) < 1:
        is_valid = False
        flash("Please enter a last name")
    if (not request.form['first_name'].isalpha()) | (not request.form['last_name'].isalpha()):
        is_valid = False
        flash("First and last names must be letters only (no numbers or special characters)")
    if len(request.form['email']) < 1:
        is_valid = False
        flash("Please enter an email")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")
    result = User.query.filter_by(email = request.form['email']).first()
    if result:
        is_valid = False
        flash("Email already exists")
    if not PASSWORD_REGEX.match(request.form['password']):
        is_valid = False
        flash("Password must have 1 uppercase alphabet, 1 lowercase alphabet, 2 digits and 1 special character. Also the minimum allowed length is 8 characters.")
    if request.form['password'] != request.form['confirm_password']:
        is_valid = False
        flash("Password/Confirm Password fields should be the same")
    if is_valid:
        flash("Friend successfully added!")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        new_instance_of_a_user = User(first_name=request.form["first_name"], last_name=request.form["last_name"], email=request.form["email"], password=pw_hash)
        db.session.add(new_instance_of_a_user)
        db.session.commit()
        session['user_id'] = new_instance_of_a_user.id
        return redirect('/quotes')
    return redirect('/')
def login():
    result = User.query.filter_by(email = request.form['email']).first()
    if result:
        if bcrypt.check_password_hash(result.password, request.form['password']):
            session['user_id'] = result.id
            return redirect('/quotes')
    flash("You could not be logged in")
    return redirect("/")
def index():
    if session.get('user_id') is None:
        return redirect('/')
    result = User.query.filter_by(id=session['user_id']).first()
    session['first_name'] = result.first_name
    quotes = Quote.query.order_by(desc(Quote.id)).all()
    return render_template('quotes.html', quotes=quotes)
def add_a_quote():
    is_valid = True
    if len(request.form["author"]) < 3:
        is_valid = False
        flash("Author must be more than 3 characters long")
    if len(request.form["quote"]) < 10:
        is_valid = False
        flash("Quote must be more than 10 characters long")
    if is_valid:
        new_instance_of_a_quote = Quote(user_id=session["user_id"], author=request.form["author"], quote=request.form["quote"])
        db.session.add(new_instance_of_a_quote)
        db.session.commit()
    return redirect('/quotes')
def like_quote(quote_id):
    existing_quote = Quote.query.get(quote_id)
    existing_user = User.query.get(session['user_id'])
    existing_user.quotes_this_user_likes.append(existing_quote)
    db.session.commit()
    return redirect('/quotes')
def user_page(user_id):
    user = User.query.get(user_id)
    quotes = user.user_quotes
    return render_template('user.html', user=user, quotes=quotes)
def myaccount(user_id):
    user = User.query.get(user_id)
    return render_template('account.html', user=user)
def edit_account():
    is_valid = True
    if len(request.form['first_name']) < 1:
        is_valid = False
        flash("Please enter a first name")
    if len(request.form['last_name']) < 1:
        is_valid = False
        flash("Please enter a last name")
    if (not request.form['first_name'].isalpha()) | (not request.form['last_name'].isalpha()):
        is_valid = False
        flash("First and last names must be letters only (no numbers or special characters)")
    if len(request.form['email']) < 1:
        is_valid = False
        flash("Please enter an email")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email address!")
    current_user = User.query.filter_by(id=session['user_id']).first()
    if not current_user.email == request.form['email']:
        search_email_in_database = User.query.filter_by(email = request.form['email']).first()
        if search_email_in_database:
            is_valid = False
            flash("Email already exists")
    if is_valid:
        user_instance_to_update = User.query.get(session['user_id'])
        user_instance_to_update.first_name = request.form['first_name']
        user_instance_to_update.last_name = request.form['last_name']
        user_instance_to_update.email = request.form['email']
        db.session.commit()
    return redirect('/myaccount/'+str(session['user_id']))
def delete_quote(quote_id):
    quote_instance_to_delete = Quote.query.get(quote_id)
    db.session.delete(quote_instance_to_delete)
    db.session.commit()
    return redirect("/quotes")
def logout():
    session.clear()
    return redirect('/')