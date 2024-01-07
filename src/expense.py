from datetime import datetime
from decimal import Decimal

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from src.auth import login_required
from src.services import data_service

bp = Blueprint('expenses', __name__)


@bp.route('/')
@login_required
def display_expenses():
    expenses_list = data_service.retrieve_expenses()
    return render_template('expenses/expenses.html', expenses=expenses_list)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create_expense():
    if request.method == 'POST':
        name = request.form['name'].strip()
        amount = request.form['amount']
        date_str = request.form['due_date']

        error = None

        if not name:
            error = 'Name is required.'
        elif not amount:
            error = 'Amount is required.'
        elif not date_str:
            error = 'Due Date is required.'

        if error is not None:
            flash(error)
        else:
            decimal_amount = Decimal(request.form['amount'])
            due_date = datetime.strptime(date_str, '%Y-%m-%d')

            error = data_service.create_expense(name=name, amount=decimal_amount, due_date=due_date)
            if error is not None:
                flash(error)
            else:
                return redirect(url_for('expenses.display_expenses'))

    return render_template('expenses/create.html')


@bp.route('/<expense_id>/update', methods=('GET', 'POST'))
@login_required
def update_expense(expense_id):
    expense = data_service.get_expense(expense_id)

    error = None

    if expense is None:
        error = 'Internal error. Please try again.'
        flash(error)
        return redirect(url_for('expenses.display_expenses'))

    if request.method == 'POST':
        name = request.form['name'].strip()
        amount = request.form['amount']
        date_str = request.form['due_date']

        if not name:
            error = 'Name is required.'
        elif not amount:
            error = 'Amount is required.'
        elif not date_str:
            error = 'Due Date is required.'

        if error is not None:
            flash(error)
        else:
            decimal_amount = Decimal(request.form['amount'])
            due_date = datetime.strptime(date_str, '%Y-%m-%d')

            error = data_service.update_expense(expense_id=expense_id, name=name, amount=decimal_amount, due_date=due_date)
            if error is not None:
                flash(error)
            else:
                return redirect(url_for('expenses.display_expenses'))

    return render_template('expenses/update.html', expense=expense)


@bp.post('/<name>/delete')
@login_required
def delete_expense(name):
    error = data_service.delete_expense(name)

    if error is not None:
        flash(error)

    return redirect(url_for('expenses.display_expenses'))
