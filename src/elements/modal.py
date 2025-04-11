from textual.screen import ModalScreen
from textual.widgets import Button
from elements.form import Form, FormRow
from elements.input_field import InputField
from textual.widgets import Input
from elements.messages import SaveRule


class Modal(ModalScreen):

    def __init__(self, widget):
        super().__init__(id="modal")
        self.widget = widget

    def compose(self):
        yield self.widget

    def on_modal_close(self, event):
        self.app.pop_screen()


class SaveModal(Modal):

    AUTO_FOCUS = "#input_name"

    def __init__(self, exp):
        input_exp = InputField(placeholder="λx.x", value=exp, id="input_exp")
        super().__init__(Form(
            FormRow("ID:", Input(placeholder="", id="input_name")),
            FormRow("Expression:", input_exp),
            right_button=Button("Save", variant="warning", id="save2")
        ))

    def submit(self):
        name = self.get_widget_by_id("input_name").value
        exp = self.get_widget_by_id("input_exp").value
        self.post_message(SaveRule(name, exp))
        self.app.pop_screen()

    def on_button_pressed(self, event):
        self.submit()

    def on_input_submitted(self, event):
        self.submit()

    def on_key(self, event):
        if event.key == "escape":
            self.app.pop_screen()
