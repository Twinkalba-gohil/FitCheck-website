from functools import wraps
from flask import session, redirect, url_for, request

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session or session.get("role") != "Admin":
            return redirect(url_for("admin.admin_login"))
        return f(*args, **kwargs)
    return decorated_function


# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if "user_id" not in session:
#             return redirect(url_for("user.login"))
#         return f(*args, **kwargs)
#     return wrap



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "u_id" not in session:
            return redirect(url_for("user.login", next=request.url))

        return f(*args, **kwargs)

    return decorated_function


# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if "user_id" not in session:
#             return redirect(url_for("user.login", next=request.url))
#         return f(*args, **kwargs)
#     return wrap