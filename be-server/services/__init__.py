from dao import *
import hashlib, os, binascii
from datetime import date


#########
#
# Users
#
#########

def service_create_user(db, user_object, new_user): 
    user_exist = dao_get_username(user_object, new_user["username"])

    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    hashed_pwd = hashlib.pbkdf2_hmac("sha512", new_user["password"].encode("utf-8"), salt, 100000)
    hashed_pwd = binascii.hexlify(hashed_pwd)

    salt_hashedpwd = (salt + hashed_pwd).decode("ascii")

    if user_exist == None:
        dao_create_user(db, user_object, username=new_user["username"].lower(), email=new_user["email"], password=salt_hashedpwd)
        data = service_get_user(user_object, new_user["username"])
        return data
    else:
        return "User Exists"

def service_login_user(user_object, login_details):
    user_exist = dao_get_username(user_object, login_details["username"].lower())

    failed_login = {"error": -1}

    if user_exist == None:
        return failed_login

    salt = user_exist.password[:64]
    stored_password = user_exist.password[64:]
    pwdhash = hashlib.pbkdf2_hmac("sha512", login_details["password"].encode("utf-8"), salt.encode("ascii"), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode("ascii")

    if pwdhash == stored_password:
        json_data = {
            "error": "",
            "user_id": user_exist.id,
            "username": user_exist.username
        }
        return json_data
    else:
        return failed_login

def service_get_user(user_object, id):

    data = dao_get_user(user_object, id)

    if data == None:
        return "User doesn't exist"

    json_data = {
    'id': data.id,
    'username': data.username,
    'email': data.email,
    'password': data.password,
    'created_at': data.created_at,
    'last_modified': data.last_modified
    }

    return json_data

#########
#
# Budget
#
#########

def service_get_budget(budget_object, user_id):
    data = dao_get_budget(budget_object, user_id)

    if data == None:
        return "Budget doesn't exist"
   
    json_data = {
        "user_id": data.user_id,
        "monthly_budget": data.monthly_budget or None,
        "groceries_alloc": data.groceries_alloc or None,
        "bills_alloc": data.bills_alloc or None,
        "transport_alloc": data.transport_alloc or None,
        "misc_alloc": data.misc_alloc or None,
        "savings_target": data.savings_target or None,
        "monthly_income": data.monthly_income or None,
        "created_at": data.created_at or None
    }

    return json_data

def service_update_user_budget(db, budget_object, user_id, json_body):
    dao_update_budget(db, budget_object, user_id, json_body["monthly_budget"], json_body["groceries_alloc"], json_body["bills_alloc"], json_body["transport_alloc"], json_body["misc_alloc"], json_body["savings_target"], json_body["monthly_income"])
    
    data = dao_get_budget(budget_object, user_id)

    json_data = {
        "user_id": data.user_id,
        "monthly_budget": data.monthly_budget or None,
        "groceries_alloc": data.groceries_alloc or None,
        "bills_alloc": data.bills_alloc or None,
        "transport_alloc": data.transport_alloc or None,
        "misc_alloc": data.misc_alloc or None,
        "savings_target": data.savings_target or None,
        "monthly_income": data.monthly_income or None,
        "created_at": data.created_at or None
    }

    return json_data

#########
#
# Expenses
#
#########

def service_create_expense(db, expense_object, user_id, new_expense):
    dao_create_expense(db, expense_object, user_id, new_expense["category_id"], new_expense["expense_description"], new_expense["amount"])

    result = dao_get_expense_by_expense_description(expense_object, new_expense["expense_description"])
    
    json_data = {
        "id": result.id,
        "user_id": result.user_id,
        "category_id": result.category_id,
        "expense_description": result.expense_description,
        "amount": result.amount,
        "created_at": result.created_at
    }

    return json_data

def service_get_expenses(expense_object, user_id):
    expenses = []

    data = dao_get_expenses(expense_object, user_id)

    if len(data) == 0:
        return "Budget doesn't exist"

    
    for expense in data:
        json_object = {
            "user_id": expense.user_id,
            "category_id": expense.category_id,
            "expense_description": expense.expense_description,
            "amount": expense.amount,
            "created_at": expense.created_at,
            "last_modified": expense.last_modified
        }
        expenses.append(json_object)

    return {"expenses": expenses}

def service_get_expense(expense_object, expense_id):
    data = dao_get_expense(expense_object, expense_id)

    if data == None:
        return "Expense doesn't exist"
    
    json_object = {
        "user_id": data.user_id,
        "category_id": data.category_id,
        "expense_description": data.expense_description,
        "amount": data.amount,
        "created_at": data.created_at,
        "last_modified": data.last_modified
    }

    return json_object

def service_update_expense(db, expense_object, user_id, json_body):
    dao_update_expense(db, expense_object, user_id, json_body["category_id"], json_body["expense_description"], json_body["amount"], date.today())
    
    data = dao_get_expense(expense_object, user_id)

    json_data = {
        "user_id": data.user_id,
        "category_id": data.category_id,
        "expense_description": data.expense_description,
        "amount": data.amount,
        "modified_at": data.modified_at
    }

    return json_data

#########
#
# Eco Goals / Actions
#
#########

def service_get_eco_goals(eco_goal_object, user_id):
    eco_goals = []

    data = dao_get_eco_goals(eco_goal_object, user_id)

    if len(data) == 0:
        return "Eco Goals don't exist"
    
    for eco_goal in data:
        json_object = {
            "goal_name": eco_goal.goal_name,
            "user_id": eco_goal.user_id,
        }
        eco_goals.append(json_object)

    return { "eco_goals": eco_goals}

def service_get_eco_actions(eco_action_object, user_id):
    eco_actions = []

    data = dao_get_eco_actions(eco_action_object, user_id)

    if len(data) == 0:
        return "Eco Actions don't exist"
    
    for eco_action in data:
        json_object = {
            "user_id": eco_action.user_id,
            "id": eco_action.id,
            "eco_goal_id": eco_action.eco_goal_id,
            "expense_id": eco_action.expense_id
        }
        eco_actions.append(json_object)

    return { "eco_actions": eco_actions}

def service_get_eco_actions(eco_action_object, user_id):
    eco_actions = []

    data = dao_get_eco_actions(eco_action_object, user_id)

    if len(data) == 0:
        return "Eco Actions don't exist"
    
    for eco_action in data:
        json_object = {
            "id": eco_action.id,
            "user_id": eco_action.user_id,            
            "eco_goal_id": eco_action.eco_goal_id,
            "expense_id": eco_action.expense_id,
            "created_at": eco_action.created_at
        }
        eco_actions.append(json_object)

    return {"eco_actions": eco_actions}
