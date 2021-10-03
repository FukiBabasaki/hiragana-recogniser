import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('pred', __name__, url_prefix='/pred')

@bp.route('/', methods = ['GET'])
def predict():
    return render_template('base.html')