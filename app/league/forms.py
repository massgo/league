# -*- coding: utf-8 -*-
"""Shared forms."""
from wtforms import Field
from wtforms.widgets import HTMLString


class CheckboxTableWidget(object):
    """Widget for rendering table with checkboxes on each row."""

    def __call__(self, field, **kwargs):
        """Render table to HTML."""
        columns = kwargs.pop('columns', field.columns)
        rows = kwargs.pop('rows', field.rows)

        html = []
        html.append('<div class="table-responsive"><table class="table '
                    'table-striped"><thead><tr><th />')
        for column in columns:
            html.append('<th>{}</th>'.format(column))
        html.append('</tr></thead><tbody>')

        for row in rows:
            html.append('<tr><td><input class="form-check-input" '
                        'type="checkbox" name="obj_id" value="{}" '
                        '/></td>'.format(row[0]))
            for value in row[1:]:
                html.append('<td>{}</td>'.format(value))
            html.append('</tr>')
        html.append('</tbody></table></div>')
        return HTMLString(''.join(html))


class CheckboxTableField(Field):
    """Field representing table with checkboxes on each row."""

    widget = CheckboxTableWidget()

    def __init__(self, columns, *args, **kwargs):
        """
        Override constructor to allow for passing of display data columns.

        Only the column titles are passed in here, as actual data will be passed
        at process time.
        """
        self.columns = columns
        self.rows = []
        super().__init__(*args, **kwargs)

    def process(self, formdata, data=None):
        """Override process method has hack around weirdness."""
        if formdata:
            self.process_formdata(formdata)
        elif data is not None:
            self.process_data(data)

    def process_data(self, data):
        """Process data rows for rendering to table."""
        row_objects = data['row_objects']
        for obj in row_objects:
            row = [obj.id]
            for field_label, field_name in self.columns.items():
                row.append(getattr(obj, field_name))
            self.rows.append(row)

    def process_formdata(self, formdata):
        """Process object IDs retrieved from form POST."""
        self.data = list(map(int, formdata.getlist('obj_id')))
