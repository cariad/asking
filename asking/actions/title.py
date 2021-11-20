from ansiscape import double_underline, heavy

from asking.actions.action import Action, ActionResult


class TitleAction(Action):
    def perform(self) -> ActionResult:
        try:
            title = self._action["title"]
        except KeyError:
            return ActionResult(next=None, recognised=False)

        self.state.out.write("\n")
        self.state.out.write(double_underline(heavy(title)).encoded)
        self.state.out.write("\n")
        return ActionResult(next=None, recognised=True)
