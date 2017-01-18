# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.css',
    'libs/font-awesome4/css/font-awesome.css',
    'libs/datatables.net-bs/css/dataTables.bootstrap.css',
    'libs/datatables.net-select-bs/css/select.bootstrap.css',
    'css/style.css',
    filters=['cssmin', 'cssrewrite'],
    output='public/css/common.css'
)

js = Bundle(
    'libs/jquery/dist/jquery.js',
    'libs/bootstrap/dist/js/bootstrap.js',
    'libs/moment/min/moment-with-locales.js',
    'libs/combodate/src/combodate.js',
    'libs/datatables.net/js/jquery.dataTables.js',
    'libs/datatables.net-bs/js/dataTables.bootstrap.js',
    'libs/datatables.net-select/js/dataTables.select.js',
    'js/plugins.js',
    filters='jsmin',
    output='public/js/common.js'
)

assets = Environment()

assets.register('js_all', js)
assets.register('css_all', css)
