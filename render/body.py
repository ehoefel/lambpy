import logging
logger = logging.getLogger(__name__)


class Body:

    def __init__(self):
        self.focus = None
        self.elements = {}
        self.input_functions = {
            65: lambda: self.move_focus("up"),
            66: lambda: self.move_focus("down"),
            67: lambda: self.move_focus("right"),
            68: lambda: self.move_focus("left")
        }

    def move_focus(self, direction):
        if direction in self.focus_map[self.focus].keys():
            next_focus = self.focus_map[self.focus][direction]
            if not self.elements[next_focus].is_enabled():
                if "disabled" in self.focus_map[next_focus].keys():
                    disabled_map = self.focus_map[next_focus]["disabled"]
                    if direction in disabled_map.keys():
                        next_focus = disabled_map[direction]
                    else:
                        return
                else:
                    return
            self.focus = next_focus

    def set_focus(self, key):
        self.focus = key

    def set_focus_map(self, focus_map):
        self.focus_map = focus_map

    def add_input_functions(self, functions):
        for key, function in functions.items():
            self.input_functions[key] = function

    def add(self, name, element):
        element.is_active = lambda: element == self.elements[self.focus]

        def render():
            return element.render()

        element.on_render(render)
        self.elements[name] = element

    def update_layout(self, layout):
        for key, element in self.elements.items():
            layout[key].update(element)

    def input(self, char):
        logger.debug(repr(char))
        if len(char) == 0:
            logger.debug("empty")
            return

        if self.focus is not None:
            focused = self.elements[self.focus]
            logger.debug("sending input to focused element " + str(focused))
            success = focused.input(char)
            if success:
                logger.debug("input returned success")
                return

        logger.debug("checking internal input functions")
        sign = ord(char)
        if sign in self.input_functions.keys():
            logger.debug("found internal input functions")
            return self.input_functions[sign]()
