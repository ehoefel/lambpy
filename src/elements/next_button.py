from textual.widgets import Button
from elements.messages import LambdaNext


class Next(Button):

    def on_click(self):
        self.post_message(LambdaNext())

    def action_press(self):
        self.post_message(LambdaNext())
