from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.user import create_user, get_user_by_email
from app.utils import verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Vérification des champs
        if not username or not email or not password:
            flash('Tous les champs sont obligatoires.', 'error')
            return render_template('auth/register.html')

        try:
            create_user(username, email, password)
            flash('Compte créé avec succès !', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Email ou username déjà utilisé.', 'error')
            return render_template('auth/register.html')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)

        if user and verify_password(password, user[3]):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard.index'))
        else:
            flash('Email ou mot de passe incorrect.', 'error')
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))