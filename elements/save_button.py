from textual.widgets import Button
from elements.messages import LambdaSave


class Save(Button):

    def on_click(self):
        self.post_message(LambdaSave())

    def action_press(self):
        self.post_message(LambdaSave())
