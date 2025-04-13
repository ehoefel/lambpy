from textual.widgets import ListView, ListItem
from elements.lambda_obj import Executable


class ReductionSteps(ListView, can_focus=False):

    def __init__(self):
        super().__init__(id="reduction_steps")

    def start(self, execution):
        self.execution = execution
        self.clear()
        renderable = Executable(execution.last_exec)
        self.append(ListItem(renderable))

    async def next_step(self):
        if not hasattr(self, "execution"):
            return
        self.execution()
        async with self.batch():
            await self.append(ListItem(Executable(self.execution.last_exec)))
        return self.scroll_end()

    def is_complete(self):
        if not hasattr(self, "execution"):
            return True
        return self.execution.is_complete()

    def get_last_step(self):
        return str(self.execution)
