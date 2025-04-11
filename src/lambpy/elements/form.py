from textual.widget import Widget
from textual.containers import Grid
from textual.widgets import Label


class FormRow():

    def __init__(self, label_text, object):
        super().__init__()
        self.label_text = label_text
        self.object = object

    def compose(self):
        yield Label(self.label_text)
        yield self.object


class Form(Widget):

    def __init__(self, *rows, left_button=None, right_button=None):
        super().__init__()
        self.rows = list(rows)
        self.left_button = left_button
        self.right_button = right_button

    def compose(self):
        rows = []
        for row in self.rows:
            rows += [Label(row.label_text), row.object]
        yield Grid(*rows)
        if self.left_button:
            yield self.left_button
        if self.right_button:
            yield Widget(self.right_button, classes="right_button")
