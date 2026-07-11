from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane
from trtextu import *

class Tramrunner(App):
    """We gonn make it"""
    CSS_FILES = [
        "trtextu/css/header_v3.tcss",
        "trtextu/css/loggerPane.tcss",
        "trtextu/css/tramcards.tcss",
        "trtextu/css/configurator.tcss"]
    CSS_PATH = CSS_FILES
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        with TabbedContent():
            with TabPane("StopInfo", id="stopinfo-wdgt"):
                yield StopInfo(id="stop-info-container")
            with TabPane("Config", id="config-pane"):
                yield Configurator(id="config-wdgt")
            with TabPane("Log", id="logger"):
                yield LoggerPane(id="logger-wdgt")

    def on_mount(self):
        poif = PointFinderConfig()
        stopinfoconfer = StopInfoConfig()
        self.config = AppConfig(poif, stopinfoconfer) # init configuration

if __name__ == "__main__":
    app = Tramrunner()
    app.run()