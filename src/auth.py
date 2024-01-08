import functools

from bson import ObjectId
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from src.services.data_service import create_user, find_user_by_username, find_user_by_id, remove_user

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register_user():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            hashed_password = generate_password_hash(password)
            created_user, error = create_user(username, hashed_password)

            if error is None:
                session.clear()
                session['user_id'] = str(created_user['id'])
                return redirect(url_for("expenses.display_expenses"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login_user():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        error = None
        user = find_user_by_username(username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = str(user['id'])
            return redirect(url_for('expenses.display_expenses'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = ObjectId(session.get('user_id'))

    if user_id is None:
        g.user = None
    else:
        g.user = find_user_by_id(user_id)


@bp.route('/logout')
def logout_user():
    session.clear()
    return redirect(url_for('auth.login_user'))


@bp.route('/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    error = remove_user(user_id)

    if error is not None:
        flash(error)
        return redirect(url_for('expenses.display_expenses'))
    else:
        session.clear()
        return redirect(url_for('auth.register_user'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login_user'))

        return view(**kwargs)

    return wrapped_view
