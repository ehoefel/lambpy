from textual.screen import Screen
from textual.containers import Grid


class Modal(Screen):

    def __init__(self, widget):
        super().__init__(id="modal")
        self.widget = widget

    def compose(self):
        yield self.widget

    def on_modal_close(self, event):
        self.app.pop_screen()
