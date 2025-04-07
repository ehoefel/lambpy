from textual.widgets import ListView, ListItem, Label


class ReductionSteps(ListView):

    def start(self, execution):
        self.execution = execution
        self.clear()
        self.append(ListItem(Label(str(execution))))

    def next_step(self):
        if not hasattr(self, "execution"):
            return
        self.execution()
        self.append(ListItem(Label(str(self.execution))))

    def is_complete(self):
        if not hasattr(self, "execution"):
            return True
        return self.execution.is_complete()
