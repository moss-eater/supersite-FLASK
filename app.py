from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, DiaryEntry

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed = generate_password_hash(request.form['password'])
        user = User(
            username=request.form['username'],
            password=hashed,
            role=request.form['role']
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'teacher':
        students = User.query.filter_by(role='student').all()
        return render_template('teacher_dashboard.html', students=students)
    else:
        entries = DiaryEntry.query.filter_by(student_id=current_user.id).all()
        return render_template('student_dashboard.html', entries=entries)

@app.route('/add_entry/<int:student_id>', methods=['GET', 'POST'])
@login_required
def add_entry(student_id):
    if current_user.role != 'teacher':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        entry = DiaryEntry(
            content=request.form['content'],
            teacher_id=current_user.id,
            student_id=student_id
        )
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('dashboard'))

    student = User.query.get(student_id)
    return render_template('add_entry.html', student=student)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
