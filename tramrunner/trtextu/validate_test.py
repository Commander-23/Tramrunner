from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane, Input, RichLog
from textual.validation import Validator, ValidationResult


class FoundStopValidator(Validator):
    def validate(self, value: str) -> ValidationResult:
        if len(value) < 10:
            return self.failure("too short")
        if set(value) - {"0", "1"}:
            return self.failure("only 0 1")
        return self.success()


class Validating(App[None]):
    """We gonn make it"""
    #CSS_FILES = ["trtextu/css/header_v3.tcss","trtextu/css/loggerPane.tcss"]
    CSS_FILES = ["css/in_valid.tcss"]
    CSS_PATH = CSS_FILES
    def compose(self) -> ComposeResult:
        yield Input(
            validators=[FoundStopValidator()],
            validate_on=["submitted"]
        )
        yield RichLog()

    @on(Input.Submitted)
    def handle_in_sub(self, event: Input.Submitted) -> None:
        rich_log = self.query_one(RichLog)
        rich_log.write(event.validation_result.is_valid)
        rich_log.write(event.validation_result.failure_descriptions)


if __name__ == "__main__":
    app = Validating()
    app.run()