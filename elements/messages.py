from textual.message import Message


class LambdaExec(Message):
    pass


class LambdaNext(Message):
    pass


class LambdaSave(Message):
    pass


class ModalClose(Message):
    pass


class SaveRule(Message):

    def __init__(self, name, expression):
        super().__init__()
        self.name = name
        self.expression = expression
    pass
