from textual import events, on

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, HorizontalGroup, Vertical, VerticalGroup, VerticalScroll
from textual.widgets import Static, Header, Footer, Label, Button, RichLog, Input, TabbedContent, TabPane, Pretty, DataTable, Digits, Collapsible, Rule, Placeholder, ListView, DataTable

from datetime import datetime
import api, utils
import time
# from stop_info_tui import stop_info_tui

class StopInfoHeader(VerticalGroup):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Input(placeholder="halte", classes="header", id="stop_info_text_input")
            yield Button("", classes="header", id="stop-info-refresh")
            yield Button("", classes="header", id="stop-info-clear")
        with HorizontalGroup():
            yield Label("_stop_place_", classes="header left", id="stop_place")
            yield Label("stop_id:", classes="header right", id="expiry1")
        with  HorizontalGroup():
            yield Label("_stop_name_", classes="header left", id="stop_name")
            yield Label("__:__:__", classes="header right", id="expiry2")


    @on(Input.Submitted, "#stop_info_text_input")
    @on(Button.Pressed, "#stop-info-refresh")
    def accept_input_vaue(self):
        self.clear_stop_info()

        # Get the stopid and with it retrive stop information
        stop_info_text_input = self.query_one("#stop_info_text_input", Input)
        stopid = utils.get_stop_id_from_pointfinder(stop_info_text_input.value)
        stop_info_data = api.vvo_departure_monitor(stopid, limit=5)

        # Write Data to the header labels
        stop_name = self.query_one("#stop_name", Label)
        stop_place = self.query_one("#stop_place", Label)
        stop_expiry1 = self.query_one("#expiry1", Label)
        stop_expiry2 = self.query_one("#expiry2", Label)
        stop_name.content = stop_info_data['Name']
        stop_place.content = stop_info_data['Place']
        stop_expiry1.content = stopid
        stop_expiry2.content = utils.vvo_time_conv(stop_info_data['ExpirationTime']).strftime("%H:%M:%S")

        # create widgets for departures
        scroller = self.app.query_one("#stop_info_scroller")
        for departure in stop_info_data['Departures']:
            new_tram = StopInfoSingleTram(classes="single_departure")
            scroller.mount(new_tram)
            scroller.scroll_visible()
            new_tram.fill_tram_info(departure)
        
        logger = self.app.query_one("#log_content", RichLog)
        logger.write(stop_info_data)


    @on(Button.Pressed, "#stop_info_clear")
    def clear_stop_info(self):
        scroller = self.app.query_one("#stop_info_scroller", VerticalScroll)
        widgets = scroller.children
        for widget in widgets:
            testies = widget
            widget.remove()

class StopInfoSingleTram(VerticalGroup):
    def compose(self) -> ComposeResult:
        with HorizontalGroup():
            yield Digits("", id="departure_line_number")
            with VerticalGroup():
                yield Static("", id="mot_type", classes="tram_info_1")
                yield Static("", id="direction_name", classes="tram_info_1")
                yield Static("", id="label4", classes="tram_info_1")
            with VerticalGroup():
                yield Static("", id="departure_time", classes="tram_info_2")
                yield Static("", id="departure_time_diff", classes="tram_info_2")
                yield Static("", id="label3", classes="tram_info_1")
            with VerticalGroup():
                yield Static("", id="departure_real_time", classes="tram_info_2")
                yield Static("", id="label1", classes="tram_info_1")
                yield Static("", id="label2", classes="tram_info_1")
        with Collapsible(title="next depa's"):
            yield DataTable()

    testies_data_arr = []
    def on_mount(self) -> None:
        compact_header = ("nr", "dir", "scheduled","DTN","Live","depaState")
        table = self.query_one(DataTable)
        table.add_columns(*compact_header)
        table.add_rows(self.testies_data_arr[0:])

    def add_row_to_table(self,):
        pass

    def fill_tram_info(self, departure_data):
        # Time Stuff
        depa_realtime = departure_data.get('RealTime')
        depa_time = departure_data.get('ScheduledTime')
        if depa_realtime:
            real_time = utils.vvo_time_conv(depa_realtime)
            time_now = datetime.now(real_time.tzinfo) if real_time.tzinfo else datetime.now()
            arrival_real_diff = real_time - time_now

            real_time_disp = real_time.astimezone().strftime("%H:%M")

            arrival_seconds = int(arrival_real_diff.total_seconds())
            if arrival_seconds <= 0:
                arrival_in = f"{arrival_seconds} sec"
            elif arrival_seconds < 60:
                arrival_in = f"{arrival_seconds} sec"
            else:
                arrival_minutes = arrival_seconds // 60
                arrival_in = f"{arrival_minutes} min"

            arrival_disp = f"{arrival_in}"
        else:
            real_time_disp = f"--:--"
            arrival_real_diff = f"--:--"
            arrival_disp = f"--:--"
            arrival_seconds = f"--:--"

        line_time = utils.vvo_time_conv(depa_time).astimezone().strftime("%H:%M")
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

        self.query_one("#departure_line_number", Digits).update(line_digits)
        self.query_one("#mot_type", Static).update(depa_mot)
        self.query_one("#direction_name", Static).update(line_direction)

        self.query_one("#departure_time"     , Static).update(f"sched: {line_time}")
        self.query_one("#departure_real_time", Static).update(f"live: {real_time_disp}")
        self.query_one("#departure_time_diff", Static).update(f"DTN: {arrival_disp}")

        self.query_one("#label1", Static).update(f"state: {depa_state}")
        #self.query_one("#label2", Static).update(f"arri_secs: {arrival_seconds}")
        #self.query_one("#label3", Static).update()

        datatable = self.query_one(DataTable)
        self.testies_data_arr.append((line_digits, line_direction, line_time, arrival_disp, real_time_disp, depa_state))
        #data_content = line_digits, depa_mot, line_direction
        #testies_dat = ["1", "zschertnitz"]
        #datatable.add_row(line_digits, depa_mot, line_direction)


class SingleTrip(HorizontalGroup):
    def compose(self) -> ComposeResult:
        with Collapsible():
            yield Label("", id="stop-name123123", classes="testies")
            yield Label("", id="stop-place123123", classes="testies")
            yield Static("Testies", classes="testies")

    def fill_trip_info(self, trip_data):
        logger = self.query_one("#log_content")



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
            with TabPane("stop-info", id="stop-info"):
                yield StopInfoHeader(id="stop_info_header")
                yield VerticalScroll(id="stop_info_scroller", classes="scroll_content")
            with TabPane("trip-search", id="trip-search"):
                yield QueryTripHeader()
                yield VerticalScroll(SingleTrip(), id="trip_info_scroller", classes="scroll_content")
                #yield VerticalScroll(RichLog, id="richlog")
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