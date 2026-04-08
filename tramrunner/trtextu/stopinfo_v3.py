from textual import on

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.reactive import reactive
from textual.validation import Length
from textual.containers import Container, VerticalScroll
from textual.widgets import Button, Input, Static, Digits, RichLog, DataTable, Switch
from textual.widgets import Label, Placeholder, Collapsible, SelectionList, Pretty, RadioSet, RadioButton
import utils, api
from datetime import datetime
import pytz

class StopInfo(Container):
    def compose(self) -> ComposeResult:
        #yield StopInfoHeader_V2(id="header-v2")
        yield StopInfoHeader_V3(id="header-v3")
        yield StopInfoContent(id="content-v2")

    def test(self):
        content_box = self.query_one("#content-log", RichLog)
        query_config = {
            'stopid': utils.get_stop_id_from_pointfinder("rac"),
            'limit': 10,
            'time': '',
            'isarrival': False,
            'shorttermchanges': False,
            'mot': ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"]
        }
        stop_info_data = api.vvo_departure_monitor(**query_config)
        self.button_clear()
        self.get_data(stop_info_data)

        depa_grouped = self.sort_depas(stop_info_data['Departures'])
        for depa_dir in depa_grouped:
            new_thing = depa_grouped[depa_dir]
            info_line = f"{new_thing[0]['LineName']} - {depa_grouped[depa_dir][0]['Direction']}"
            info_count = f"{len(new_thing)}"
            content_box.write(info_line)
            content_box.write(info_count)

        table = self.query_one("#test-tt", DataTable)
        table.add_columns("Id", "Number", "Name")
        rows = []
        for key, group in depa_grouped.items():
            rows.append((f"[b]--- {key} ---[/b]", "", ""))
            for item in group:
                rows.append((
                    utils.diff_to_now(item["ScheduledTime"]),
                    item["LineName"],
                    item["Direction"]
                ))
        for row in rows:
            table.add_row(*row)
        self.sort_depas(stop_info_data['Departures'])

    def get_data(self, query_text):
        # assemble config and query departure monitor
        query_config = {
            'stopid': utils.get_stop_id_from_pointfinder(query_text),
            'limit': 20,
            'time': '',
            'isarrival': False,
            'shorttermchanges': False,
            'mot': ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train"]#, "Cableway", "Ferry", "HailedSharedTaxi"]
        }
        stop_data = api.vvo_departure_monitor(**query_config)

        depa_grouped = self.sort_depas(stop_data['Departures'])
        header = self.query_one("#header-v3", StopInfoHeader_V3)
        
        header.stop_name = stop_data['Name']
        header.stop_place = stop_data['Place']
        header.stop_expiry = utils.diff_to_now(stop_data['ExpirationTime'])

        self.app.query_one("#content-log", RichLog).write(stop_data)

    def sort_depas(self, departures)->dict:
        depa_grouped = {}
        for departure in departures:
            depa_key = departure['Id']
            if depa_key not in depa_grouped:
                depa_grouped[depa_key] = []
            depa_grouped[depa_key].append(departure)
        return depa_grouped


class SiConfig(ModalScreen):
    def __init__(self, name = None, id = None, classes = None, stops_only = False, regional_only = False, stop_shortcuts = False):
        self.stops_only = stops_only
        self.regional_only = regional_only
        self.stop = stop_shortcuts
        super().__init__(name, id, classes)
    def compose(self) -> ComposeResult:
        with VerticalScroll(id="config-modal"):
            with Container(id="config-buttons-wq"):
                yield Static("")
                yield Button("Exit", disabled=False, id="button-conf-exit", variant="error")
                yield Static("")
                yield Button("Save", disabled=False, id="button-conf-save", variant="success")
                yield Static("")
            with Container(id="conf-stop-finder"):
                with Container(id="conf-stop-finder-switches"):
                    yield Switch(value=self.stops_only, animate=False, id="stops-only")
                    yield Static("stops-only:", classes="label")
                    yield Switch(value=self.regional_only, animate=False, id="regional-only")
                    yield Static("regional-only", classes="label")
                    yield Switch(value=self.stop, animate=False, id="stop-shortcuts")
                    yield Static("stop-shortcuts", classes="label")
                with Container(id="conf-stop-finder-limit"):
                    yield Button("+", compact=True, id="conf_stop-finder-plus")
                    yield Digits("10")
                    yield Button("-", compact=True, id="conf_stop-finder-minus")


            #yield SelectionList[int](  
            #    ("󰿧 Tram ", 0, True),
            #    ("󰃧 Bus  ", 1, True),
            #    (" Bahn ", 2, True),
            #    ("󰣄 Zug  ", 3, True),
            #    (" SSB  ", 4, False),
            #    ("󰈓 Fähr ", 5, False),
            #    ("󰓿 taxi ", 6, False),
            #    id="mot-selector",
            #)

    @on(Button.Pressed, "#button-conf-save")
    def button_conf_save(self, event):
        self.stops_only = self.query_one("#stops-only", Switch).value
        settings = {
            'stops-only': self.query_one("#stops-only", Switch).value,
            'regional-only': self.query_one("#regional-only", Switch).value,
            'stop-shortcuts': self.query_one("#stop-shortcuts", Switch).value,
        }
        self.dismiss(settings)

    @on(Button.Pressed, "#button-conf-exit")
    def button_conf_exit(self, event):
        settings = {
            'stops-only': self.stops_only,
            'regional-only': self.regional_only,
            'stop-shortcuts': self.stop
        }
        self.dismiss(settings)


class StopInfoContent(Container):
    def compose(self) -> ComposeResult:
        yield RichLog(id="content-log")
        yield DataTable(id="test-tt")


class StopInfoHeader_V3(Container):
    error_msg = reactive("")
    stop_place = reactive("")
    stop_name = reactive("")
    stop_expiry = reactive("")
    conf_poif_stops_only = reactive(False)
    conf_poif_regional_only = reactive(False)
    conf_poif_stop_shortcuts = reactive(False)
    settings = reactive([])

    def render(self):
        self.query_one("#disp-err", Static).update(self.error_msg)
        self.query_one("#disp-place", Static).update(self.stop_place)
        self.query_one("#disp-name", Static).update(self.stop_name)
        self.query_one("#disp-exp", Static).update(self.stop_expiry)
        return super().render()

    def compose(self) -> ComposeResult:
        yield Input(
            id="stop-info-text-input",
            placeholder="Enter a stop",
            validators=[Length(minimum=3, maximum=None, failure_description="min 3 char")],
            )
        yield Button("\nrfrsh", id="button-refresh", variant="success")
        yield Button("\nclear", id="button-clear", variant="primary")
        yield Button("\nconf", id="button-conf-show", variant="primary")
        yield Static(classes="err alt", id="disp-err")
        yield Static(classes="place", id="disp-place")
        yield Static("󰰂",classes="icon", id="disp-icon")
        yield Static(classes="name", id="disp-name")
        yield Static(classes="time alt", id="disp-exp")


    @on(Input.Submitted, "#stop-info-text-input")
    @on(Button.Pressed, "#button-refresh")
    def button_refresh(self):
        """get the info from input-field and pass it up(DOM) to stopinfo"""
        query_text_val = self.query_one("#stop-info-text-input", Input).value
        self.parent.get_data(query_text=query_text_val)

    @on(Button.Pressed, "#button-clear")
    def button_clear(self):
        """clear"""
        self.stop_name = "[i][b]stop-name[/b][/i]"
        self.stop_place = "[i]city[/i]"
        self.stop_expiry = "[i]expiry[/i]"

    @on(Button.Pressed, "#button-conf-show")
    def button_conf_show(self):
        config_menu = SiConfig(
            id = "stop-info-config-modal",
            stops_only = self.conf_poif_stops_only,
            regional_only = self.conf_poif_regional_only,
            stop_shortcuts = self.conf_poif_stop_shortcuts
        )
        self.app.push_screen(config_menu, self.read_config_change)

    def read_config_change(self, settings):
        self.settings = settings
        self.conf_poif_stops_only = settings['stops-only']
        self.conf_poif_regional_only = settings['regional-only']
        self.conf_poif_stop_shortcuts = settings['stop-shortcuts']
        self.app.query_one("#content-log", RichLog).write(settings)

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        if not event.validation_result.is_valid:  
           self.error_msg = str(event.validation_result.failure_descriptions)
        else:
            self.error_msg = ""