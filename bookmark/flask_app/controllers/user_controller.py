from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/login')
def login_and_reg():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        flash('You must be logged in to view your lists.')
        return redirect('/')
    # data = {
    #     'username' : request.form['username']
    # }
    
    # logged_in_user = User.get_one_by_username(data)

    return render_template('dashboard.html')

@app.route('/register', methods=['POST'])
def register():
    
    if not User.validate_user(request.form):
        return redirect('/login')
    
    hash = bcrypt.generate_password_hash(request.form['password'])
    print(hash)
    
    data = {
        **request.form,
        'password':hash
    }
    
    id = User.create(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/loginuser', methods=['POST'])
def login():
    data = {
        'username':request.form['username']
    }
    
    found_user = User.get_one_by_username(data)
    
    if not found_user:
        flash('Invalid login.', 'login')
        return redirect('/login')
    if not bcrypt.check_password_hash(found_user.password, request.form['password']):
        flash('Invalid login.', 'login')
        return redirect('/login')
    
    session['user_id'] = found_user.username
    
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')