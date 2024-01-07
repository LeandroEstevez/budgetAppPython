from decimal import Decimal
from datetime import datetime
from typing import List, Any

from bson import ObjectId
from flask import g
from mongoengine import OperationError, NotUniqueError, ValidationError

from src.models.expense import Expense
from src.models.user import User


def create_expense(name: str, amount: Decimal, due_date: datetime) -> str | None:
    expense = Expense(name=name, amount=amount, due_date=due_date)
    g.user.expenses.append(expense)

    try:
        g.user.save()
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return "Provided data is not valid."
    except OperationError as e:
        print(f"Database Operation Error: {e}")
        return "Internal error. Please try again."

    return None


def retrieve_expenses() -> List[Expense]:
    return g.user.expenses


def get_expense(expense_id: str) -> Expense | None:
    obj_id = ObjectId(expense_id)

    for exp in g.user.expenses:
        if exp["id"] == obj_id:
            return exp

    return None


def update_expense(expense_id: str, name: str, amount: Decimal, due_date: datetime) -> str | None:
    obj_id = ObjectId(expense_id)

    for exp in g.user.expenses:
        if exp["id"] == obj_id:
            exp["name"] = name
            exp["amount"] = amount
            exp["due_date"] = due_date

            try:
                g.user.save()
            except ValidationError as e:
                print(f"Validation Error: {e}")
                return "Provided data is not valid."
            except OperationError as e:
                print(f"Database Operation Error: {e}")
                return "Internal error. Please try again."

            return None

    print("Database Operation Error: Expense not found")
    return "Internal error. Please try again."


def delete_expense(expense_id: str) -> str | None:
    obj_id = ObjectId(expense_id)

    for exp in g.user.expenses:
        if exp["id"] == obj_id:
            g.user.expenses.remove(exp)

            g.user.save()
            return None

    print("Database Operation Error: Expense not found")
    return "Internal error. Please try again."


def create_user(username: str, password: str) -> (User, str):
    user = User(username=username, password=password)

    try:
        user.save()
    except NotUniqueError as e:
        print(f"Document with same values already exists: {e}")
        return None, "Username already exists."
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return None, "Provided data is not valid."
    except OperationError as e:
        print(f"Database Operation Error: {e}")
        return None, "Internal error. Please try again."

    return user, None


def remove_user(user_id: str) -> str | None:
    user = User.objects(id=user_id).first()

    if user:
        user.delete()
        return None
    else:
        print("Database Operation Error: User not found")
        return "Internal error. Please try again."


def find_user_by_username(username: str) -> User:
    user = User.objects().filter(username=username).first()
    return user


def find_user_by_id(user_id: ObjectId) -> User:
    user = User.objects(id=user_id).first()
    return user
