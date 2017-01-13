# -*- coding: utf-8 -*-
"""Shared forms."""
from flask_wtf import FlaskForm
from wtforms import Field, IntegerField
from wtforms.widgets import HTMLString


class CheckboxTableWidget(object):
    def __call__(self, field, **kwargs):
        columns = kwargs.pop('columns', field.columns)
        rows = kwargs.pop('rows', field.rows)
        button_text = kwargs.pop('button_text', field.button_text)

        html = []
        html.append('<div class="table-responsive"><table class="table '
                    'table-striped"><thead><tr><th />')
        for column in columns:
            html.append('<th>{}</th>'.format(column))
        html.append('</tr></thead><tbody>')

        row_ctr = 0
        for row in rows:
            html.append('<tr><td><input class="form-check-input" '
                        'type="checkbox" name="row_id" value="{}" '
                        '/></td>'.format(row_ctr))
            for value in row:
                html.append('<td>{}</td>'.format(value))
            html.append('</tr>')
        html.append('</tbody></table></div><button type="submit" '
                    'class="btn btn-default">{}</button>'.format(button_text))
        return HTMLString(''.join(html))


class CheckboxTableField(Field):
    widget = CheckboxTableWidget()

    def __init__(self, label='', validators=None, **kwargs):
        super().__init__(self, label, validators, **kwargs)
        _form = kwargs['_form']
        self.columns = kwargs.pop('columns', _form.columns)
        self.rows = kwargs.pop('rows', _form.rows)
        self.url = kwargs.pop('url', _form.url)
        self.button_text = kwargs.pop('button_text', _form.button_text)


class CheckboxTableForm(FlaskForm):
    table = CheckboxTableField()

    def __init__(self, *args, **kwargs):
        self.columns = kwargs.pop('columns', [])
        self.rows = kwargs.pop('rows', [])
        self.url = kwargs.pop('url', '')
        self.button_text = kwargs.pop('button_text', '')
        super().__init__(*args, **kwargs)
