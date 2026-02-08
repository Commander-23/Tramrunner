from textual import events, on

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical, VerticalGroup, VerticalScroll
from textual.widgets import Static, Header, Footer, Label, Button, RichLog, Input, TabbedContent, TabPane, Pretty, DataTable

import api, utils
import time
# from stop_info_tui import stop_info_tui

class SingleTram(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label("", id="stop-name")
            yield Label("", id="stop-place")
            yield Static("Testies", classes="testies")

class Tramrunner(App):
    """We gonn make it"""
    CSS_PATH = "textual/dom1.tcss"
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with TabbedContent():
            with TabPane("stop-info", id="stop-info"):
                yield Input(placeholder="start")
                yield VerticalScroll(SingleTram())#,SingleTram(),SingleTram(),SingleTram(),)
            with TabPane("Trip", id="trip-page"):
                yield Container(
                    Vertical(
                        Input(placeholder="test"),
                        Input(placeholder="stop"),
                        Static("HI")
                    ),
                    id="text-input"
                )
    @on(Input.Submitted)
    def accept_input_vaue(self):
        input = self.query_one(Input)
        stop_name = self.query_one("#stop-name", Label)
        stop_place = self.query_one("#stop-place", Label)
        
        stopid = utils.get_stop_id_from_pointfinder(input.value)
        stop_info_data = api.vvo_departure_monitor(stopid)

        stop_name.content = stop_info_data['Name']
        stop_place.content = stop_info_data['Place']
        self.mount(Pretty(stop_info_data))
        input.value = stopid

        
    
if __name__ == "__main__":
    app = Tramrunner()
    app.run()