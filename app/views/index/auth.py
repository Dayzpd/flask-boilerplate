from flask import redirect, render_template, request, session, url_for
from functools import wraps
from app.blueprints import index_auth
from app.models.__init__ import db
from app.models.users import Users


@index_auth.route('/login', methods=['GET', 'POST'])
def login():
    '''
    GET: Render login card.
    POST: Authenticate user.
    '''
    if request.method == 'GET':
        return render_template(
            'index_auth.html',
            content={'auth_type': 'Login'},
            notification=None
        )
    else:
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if not user:
            return render_template(
                'index_auth.html',
                content=None,
                notification={'msg': 'User does not exist.'}
            )

        success = user.check_password(password)
        if success:
            session['user'] = user.get_id()
            return render_template(
                'index_dashboard.html',
                content=None,
                notification={'msg': 'Login successful.'}
            )
        else:
            return render_template(
                'index_auth.html',
                content=None,
                notification={'msg': 'Incorrect password.'}
            )


@index_auth.route('/register', methods=['POST'])
def register():
    '''
    Create new user.
    Args:
        - email (REQUIRED): Email of new user.
        - password (REQUIRED): Password of new user.
    '''
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as err:
        return render_template(
            'index_auth.html',
            content={'auth_type': 'Register'},
            notification={
                'msg': 'Registration failed. Email or password not found in ' +
                       'POST data.'
            }
        )

    user_exists = Users.user_exists(email)
    if user_exists:
        return render_template(
            'index_auth.html',
            content={'auth_type': 'Register'},
            notification={
                'msg': 'Registration failed. Email already exists.'
            }
        )

    try:
        new_user = Users(email, password)
        db.session.add(new_user)
        db.session.commit()
    except Exception as err:
        print(str(err))
        return render_template(
            'index_auth.html',
            content={'auth_type': 'Register'},
            notification={'msg': 'Registration failed.'}
        )

    session['user'] = new_user.get_id()

    return render_template(
        'index_home.html',
        content=None,
        notification={'msg': 'Registered successfully.'}
    )


@index_auth.route('/logout')
def logout():
    '''
    Logout user.
    '''
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('index.home.landing'))


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('index.auth.login'))
        return func(*args, **kwargs)
    return decorated_function
