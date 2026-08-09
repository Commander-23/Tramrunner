from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Vertical, HorizontalGroup
from textual.widgets import Button, RichLog

class LoggerPane(Container):
    def compose(self) -> ComposeResult:
        yield Button("Clear", classes="button-clear", id="log1_clear_button")
        yield Button("\nconf", id="button-conf-show", variant="primary")
        self.logger = RichLog(id="log1_content", highlight=True, markup=True)
        yield self.logger

    @on(Button.Pressed, "#log1_clear_button")
    def clear_logger1(self):
        self.logger.clear()

    @on(Button.Pressed, "#button-conf-show")
    def button_conf_show(self):
        self.logger.write(self.app.config)
