from textual import events, on

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical, VerticalGroup, VerticalScroll
from textual.widgets import Static, Header, Footer, Label, Button, RichLog, Input, TabbedContent, TabPane, Pretty, DataTable, Digits

import api, utils
import time
# from stop_info_tui import stop_info_tui

class StopInfoHeader(VerticalGroup):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
                yield Input(placeholder="halte", classes="header", id="stop_info_text_input")
                yield Button("Clear", classes="clear_buttons", id="stop_info_clear")
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
        yield Digits("", id="departure_line_number")
        with VerticalGroup():
            yield Label("label", id="label1", classes="tram_label")
            yield Label("label", id="label2", classes="tram_label")
            yield Label("label", id="label3", classes="tram_label")
        with VerticalGroup():
            yield Static("", id="departure_time", classes="tram_label")
            yield Static("", id="departure_real_time", classes="tram_label")
            yield Label("label", id="label11", classes="tram_label")
        with VerticalGroup():
            yield Static("", id="mot_type", classes="tram_label")
            yield Static("", id="direction_name", classes="tram_label")

    
    def fill_tram_info(self, departure_data):
        
        # Time Stuff
        depa_realtime = departure_data.get('RealTime')
        depa_time = departure_data.get('ScheduledTime')
        if depa_realtime: real_time = utils.vvo_time_conv(depa_realtime).strftime("%H:%M")
        else: real_time = f"--:--"
        line_time = utils.vvo_time_conv(depa_time).strftime("%H:%M")
        depa_state = departure_data.get('State')
        # ID Stuff
        depa_id = departure_data.get('Id')    
        depa_dlid = departure_data.get('DlId')    
        depa_diva = departure_data.get('Diva')

        # schedule stuff
        depa_routechanges = departure_data.get('RouteChanges')
        depa_ocup = departure_data.get('Occupancy')            
        depa_cancel_res = departure_data.get('CacelReasons')

        # line info stuff    
        depa_mot = departure_data.get('Mot')
        line_name = departure_data.get('LineName')
        line_direction = departure_data.get('Direction')
        depa_platform = departure_data.get('Platform')
        
        # seperating line_name into digits and charachters
        line_digits = "".join([char for char in line_name if char.isdigit()])
        line_char = "".join([char for char in line_name if char.isalpha()])

        self.query_one("#label1", Label).update(f"{"".join(line_digits)}")
        self.query_one("#label2", Label).update(f"{"".join(line_char)}")

        self.query_one("#departure_line_number", Digits).update(line_digits)
        self.query_one("#direction_name", Static).update(line_direction)
        self.query_one("#mot_type", Static).update(depa_mot)
        self.query_one("#departure_time", Static).update(f"{real_time} live")
        self.query_one("#departure_real_time", Static).update(f"{line_time}")
        
class SingleTram(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with VerticalGroup():
            yield Label("", id="stop-name")
            yield Label("", id="stop-place")
            yield Static("Testies", classes="testies")


class QueryTripHeader(VerticalGroup):
    def compose(self) -> ComposeResult:
            with HorizontalGroup():
                yield Input(placeholder="start", classes="header", id="trip_userin_start")
                yield Input(placeholder="stop", classes="header", id="trip_userin_stop")
            with HorizontalGroup():
                yield Button("Submit", id="trip_submit")
                yield Button("Clear", id="trip_clear")
                with VerticalGroup():
                    yield Static("label")
                    yield Static("label")
                    yield Static("label")
            

class Tramrunner(App):
    """We gonn make it"""
    CSS_PATH = "textual/dom1.tcss"
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with TabbedContent():
            with TabPane("stop-info", id="pane_stop_info"):
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
        stop_info_data = api.vvo_departure_monitor(stopid, limit=30)

        stop_name.content = stop_info_data['Name']
        stop_place.content = stop_info_data['Place']
        stop_expiry1.content = stopid
        stop_expiry2.content = utils.vvo_time_conv(stop_info_data['ExpirationTime']).strftime("%H:%M:%S")
        logger.write(stop_info_data)

        for departure in stop_info_data['Departures']:

            new_tram = StopInfoSingleTram(classes="single_departure")
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