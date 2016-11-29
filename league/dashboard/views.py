# -*- coding: utf-8 -*-
"""Dashboard."""
from flask import Blueprint, render_template

blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard', static_folder='../static')


@blueprint.route('/')
def dashboard():
    """Dashboard."""
    headers = ['White', 'Black', 'Winner', 'Handicap', 'Komi']
    data = [
                ['Andrew Hall', 'Milan Mladenovic', 'White', 5, 0]
            ]
    return render_template('dashboard/dashboard.html', headers=headers, data=data)
