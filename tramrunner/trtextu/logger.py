from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Vertical
from textual.widgets import Button, Input, Static, Digits, RichLog, Label

class LoggerPane(Container):
    def compose(self) -> ComposeResult:
        yield Button("Clear", classes="button-clear", id="log1_clear_button")
        yield Label("logger 1\n#log1_content")
        yield RichLog(id="log1_content", highlight=True, markup=True)


    @on(Button.Pressed, "#log1_clear_button")
    def clear_logger1(self):
        logger = self.query_one("#log1_content")
        logger.clear()
