from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models.group import create_group, get_group_by_code, join_group, get_user_groups, get_group_members
from app.models.message import get_group_messages

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@dashboard_bp.route('/dashboard')
@login_required
def index():
    groups = get_user_groups(session['user_id'])
    return render_template('dashboard/index.html', groups=groups)

@dashboard_bp.route('/group/create', methods=['POST'])
@login_required
def create():
    name = request.form.get('name')
    if not name:
        flash('Le nom du groupe est obligatoire.', 'error')
        return redirect(url_for('dashboard.index'))
    invite_code = create_group(name, session['user_id'])
    flash(f'Groupe créé ! Code d\'invitation : {invite_code}', 'success')
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/group/<int:group_id>')
@login_required
def group(group_id):
    from app.models.group import get_group_by_id
    grp = get_group_by_id(group_id)
    if not grp:
        return redirect(url_for('dashboard.index'))
    members = get_group_members(group_id)
    messages = get_group_messages(group_id)
    return render_template('dashboard/chat.html',
        group_id=group_id,
        group_name=grp[1],
        invite_code=grp[2],
        members=members,
        messages=messages,
        username=session['username']
    )

@dashboard_bp.route('/group/join', methods=['POST'])
@login_required
def join():
    invite_code = request.form.get('invite_code')
    group = get_group_by_code(invite_code)
    if not group:
        flash('Code d\'invitation invalide.', 'error')
        return redirect(url_for('dashboard.index'))
    joined = join_group(group[0], session['user_id'])
    if not joined:
        flash('Vous êtes déjà membre de ce groupe.', 'error')
    else:
        flash(f'Vous avez rejoint {group[1]} !', 'success')
    return redirect(url_for('dashboard.index'))

