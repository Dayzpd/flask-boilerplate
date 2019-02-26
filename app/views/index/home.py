from flask import render_template, session, request

from app.blueprints import index_home


@index_home.route('/', methods=['GET'])
def landing():
    '''
    Render index template.
    '''
    print(request)
    print(request.environ['REMOTE_ADDR'])
    if 'user' in session:
        logged_in = True
    else:
        logged_in = False
    return render_template(
        'index_template.html',
        content={'logged_in': logged_in},
        notification=None
    )
