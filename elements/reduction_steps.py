from textual.widgets import ListView, ListItem, Label


class ReductionSteps(ListView):

    def add_step(self, step):
        self.append(ListItem(Label(step)))
