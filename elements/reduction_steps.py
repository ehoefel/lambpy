from textual.widgets import ListView, ListItem
from elements.lambda_obj import Executable


class ReductionSteps(ListView):

    def start(self, execution):
        self.execution = execution
        self.clear()
        renderable = Executable(execution.last_exec)
        self.append(ListItem(renderable))

    def next_step(self):
        if not hasattr(self, "execution"):
            return
        self.execution()
        self.append(ListItem(Executable(self.execution.last_exec)))
        self.scroll_end()

    def is_complete(self):
        if not hasattr(self, "execution"):
            return True
        return self.execution.is_complete()

    def get_last_step(self):
        return str(self.execution)
