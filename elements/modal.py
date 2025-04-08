from textual.screen import ModalScreen
from elements.form import Form, FormRow
from elements.input_field import InputField


class Modal(ModalScreen):

    def __init__(self, widget):
        super().__init__(id="modal")
        self.widget = widget

    def compose(self):
        yield self.widget

    def on_modal_close(self, event):
        self.app.pop_screen()


class SaveModal(Modal):

    AUTO_FOCUS = "#exp_id"

    def __init__(self, exp):
        super().__init__(Form(
            FormRow("ID:", InputField(placeholder="", id="exp_id")),
            FormRow("Expression:", InputField(placeholder="λx.x", value=exp))
        ))
