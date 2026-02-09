from textual import events, on

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical, VerticalGroup, VerticalScroll
from textual.widgets import Static, Header, Footer, Label, Button, RichLog, Input, TabbedContent, TabPane, Pretty, DataTable, Digits

import api, utils
import time
# from stop_info_tui import stop_info_tui

class StopInfoHeader(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield VerticalGroup(
            Label("_stop_name_", classes="header", id="stop-name"),
            Label("_stop_place_", classes="header", id="stop-place")
        )
        yield VerticalGroup(
            Label("Expiry Time:", classes="header", id="expiry1"),
            Label("__:__:__", classes="header", id="expiry2")
        )

class StopInfoSingleTram(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield Digits("", id="departure_number_name")
        with VerticalGroup():
            yield Static("", id="departure_time", classes="tram_label")
            yield Static("", id="departure_real_time", classes="tram_label")
        with VerticalGroup():
            yield Static("", id="mot_type", classes="tram_label")
            yield Static("", id="direction_name", classes="tram_label")
        with VerticalGroup():
            yield Label("label", classes="tram_label")
            yield Label("label", classes="tram_label")

    
    def fill_tram_info(self, departure_data):
        if 'RealTime' in departure_data:
            real_time = utils.vvo_timestamp_to_datetime_class(departure_data['RealTime']).strftime("%H:%M")
        else: real_time = f"--:--"
        depa_time = utils.vvo_timestamp_to_datetime_class(departure_data['ScheduledTime']).strftime("%H:%M")

        self.query_one("#departure_number_name", Digits).update(departure_data['LineName'])
        self.query_one("#direction_name", Static).update(departure_data['Direction'])
        self.query_one("#mot_type", Static).update(departure_data['Mot'])
        self.query_one("#departure_time", Static).update(f"{real_time} live")
        self.query_one("#departure_real_time", Static).update(f"{depa_time}")
        
class SingleTram(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label("", id="stop-name")
            yield Label("", id="stop-place")
            yield Static("Testies", classes="testies")


class QueryTripHeader(HorizontalGroup):
    def compose(self) -> ComposeResult:
            yield Label("HI")
            

class Tramrunner(App):
    """We gonn make it"""
    CSS_PATH = "textual/dom1.tcss"
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with TabbedContent():
            with TabPane("stop-info", id="pane_stop_info"):
                yield Input(placeholder="start", classes="header", id="stop_info_text_input")
                yield StopInfoHeader()
                yield VerticalScroll(id="stop_info_scroller")
            with TabPane("Trip", id="trip-page"):
                yield QueryTripHeader()
                #yield VerticalScroll(RichLog, id="richlog")
            with TabPane("Log", id="logger"):
                with Vertical():
                    yield Button("Clear", id="log_clear_button")
                    yield RichLog(id="log_content")


    @on(Input.Submitted, "#stop_info_text_input")
    def accept_input_vaue(self):

        # Input & Header Label's
        stop_info_text_input = self.query_one("#stop_info_text_input", Input)
        stop_name = self.query_one("#stop-name", Label)
        stop_place = self.query_one("#stop-place", Label)
        stop_expiry1 = self.query_one("#expiry1", Label)
        stop_expiry2 = self.query_one("#expiry2", Label)
        logger = self.query_one("#log_content")
        scroller = self.query_one("#stop_info_scroller")

        #
        stopid = utils.get_stop_id_from_pointfinder(stop_info_text_input.value)
        stop_info_data = api.vvo_departure_monitor(stopid)

        stop_name.content = stop_info_data['Name']
        stop_place.content = stop_info_data['Place']
        stop_expiry1.content = stopid
        stop_expiry2.content = utils.vvo_timestamp_to_datetime_class(stop_info_data['ExpirationTime']).strftime("%H:%M:%S")
        logger.write(stop_info_data)

        for departure in stop_info_data['Departures']:
            new_tram = StopInfoSingleTram()
            scroller.mount(new_tram)
            scroller.scroll_visible()
            new_tram.fill_tram_info(departure)
        #input.value = stopid

    @on(Button.Pressed, "#log_clear_button")
    def clear_log_page(self):
        logger = self.query_one("#log_content")
        logger.clear()
    
if __name__ == "__main__":
    app = Tramrunner()
    app.run()