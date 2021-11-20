from asking.actions.action import Action, ActionResult


class TextAction(Action):
    def perform(self) -> ActionResult:
        try:
            text = self._action["text"]
        except KeyError:
            return ActionResult(next=None, recognised=False)

        self.state.out.write("\n")
        self.state.out.write(text)
        self.state.out.write("\n")
        return ActionResult(next=None, recognised=True)
