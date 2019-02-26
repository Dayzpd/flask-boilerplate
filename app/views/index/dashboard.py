from flask import redirect, render_template, request, session, url_for

from app.blueprints import index_dashboard
from app.views.index.auth import login_required


@index_dashboard.route('/', methods=['GET'])
def dashboard():
    '''
    Render index template.
    '''
    return render_template(
        'index_dashboard.html',
        content=None,
        notification=None
    )
