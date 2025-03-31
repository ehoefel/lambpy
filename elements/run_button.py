from textual.widgets import Button
from elements.messages import LambdaExec


class Run(Button):

    def on_click(self):
        self.post_message(LambdaExec())

    def action_press(self):
        self.post_message(LambdaExec())
