from flask import Blueprint, redirect


bp = Blueprint('frontend', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return redirect('api')



