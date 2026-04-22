from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane
from trtextu import *

class Tramrunner(App):
    """We gonn make it"""
    CSS_FILES = ["trtextu/css/header_v3.tcss","trtextu/css/loggerPane.tcss"]
    CSS_PATH = CSS_FILES
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with TabbedContent():
            with TabPane("StopInfo", id="stopinfo-wdgt"):
                yield StopInfo(id="stop-info-container")
            with TabPane("Log", id="logger"):
                yield LoggerPane(id="logger-wdgt")

if __name__ == "__main__":
    app = Tramrunner()
    app.run()