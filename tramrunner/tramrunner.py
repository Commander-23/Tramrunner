from textual import events, on

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical, VerticalGroup, VerticalScroll
from textual.widgets import Static, Header, Footer, Label, Button, RichLog, Input, TabbedContent, TabPane, Pretty, DataTable, Digits, Collapsible, Rule, Placeholder, ListView, DataTable

from trtextu import *

from datetime import datetime
import api, utils
import time


class Tramrunner(App):
    """We gonn make it"""
    CSS_PATH = "trtextu/css/header_v3.tcss"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with TabbedContent():
            with TabPane("v2", id="sih-v2"):
                yield StopInfo(id="stop-info-container")
            #with TabPane("Testies", id="tester"):
            #   yield StopInfoHeader_V3(id="header-v3")
            with TabPane("Log", id="logger"):
                with Vertical():
                    yield Button("Clear", id="log_clear_button")
                    yield RichLog(id="log_content")

    @on(Button.Pressed, "#log_clear_button")
    def clear_log_page(self):
        logger = self.query_one("#log_content")
        logger.clear()


if __name__ == "__main__":
    app = Tramrunner()
    app.run()