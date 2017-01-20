# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.css',
    'libs/font-awesome/css/font-awesome.css',
    'libs/agrotable/compiled/footable.*.min.css',
    'css/style.css',
    filters=['cssmin', 'cssrewrite'],
    output='public/css/common.css'
)

js = Bundle(
    'libs/jquery/dist/jquery.js',
    'libs/bootstrap/dist/js/bootstrap.js',
    'libs/moment/min/moment-with-locales.js',
    'libs/combodate/src/combodate.js',
    'libs/agrotable/compiled/footable.*.min.js',
    'js/plugins.js',
    filters='jsmin',
    output='public/js/common.js'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
