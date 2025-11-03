from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Project, Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'password'

# Bind Flask app to SQLAlchemy
db.init_app(app)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        #get form data
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            flash("Password and Confirm Password didn't match!")
            return redirect(url_for('register'))

        #check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("username already exists!")
            return redirect(url_for('register'))

        #password hash
        hashed_password = generate_password_hash(password)

        if password != password2:
            flash("Password and Confirm Password didn't match!")
            return redirect(url_for('register'))

        #creating new user
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration succesful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    # Render login form or handle login logic
    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)