from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.validation import Length
from textual.containers import Container, VerticalScroll, Horizontal, HorizontalGroup
from textual.widgets import Button, Input, Static, Digits, RichLog, DataTable, Switch
from textual.widgets import Label, Placeholder, Collapsible, SelectionList, Pretty, RadioSet, RadioButton

from .daclas import *
import utils, api
from datetime import datetime, time
import pytz
from .tramcards_test import TramCardBig

class StopInfo(Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.widgets_disp = []
        self.new_conf = {
            "poifi_limit"  : 0,
            "stopsOnly"    : False,
            "regionalOnly" : False,
            "stopShortcuts": False,
        }
    def compose(self) -> ComposeResult:
        #yield StopInfoHeader_V2(id="header-v2")
        yield StopInfoHeader_V3(id="header-v3")
        yield StopInfoContent(id="content-v2")


    @on(Button.Pressed, "#button-clear")
    def button_clear(self):
        header = self.query_one("#header-v3", StopInfoHeader_V3)
        header.clear_header_info()
        for child in self.widgets_disp:
            child.remove()

    @on(Button.Pressed, "#button-refresh")
    @on(Input.Submitted, "#stop-info-text-input")
    def process_search_input(self):
        self.button_clear()
        stop_info_config = DepaMonConfig(
            #query_text="rac",
            limit=self.app.config.stopInfo.limit,
            time ="",
            isarrival=False,
            shorttermchanges=False,
            mot=["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train"],#, "Cableway", "Ferry", "HailedSharedTaxi"]
            )
        stop_info_config.query_text = self.query_one("#stop-info-text-input", Input).value
        logger = self.app.query_one("#log1_content", RichLog)
        header = self.query_one("#header-v3", StopInfoHeader_V3)
        content = self.parent.query_one("#SICScroller", VerticalScroll)
        stop_data = api.vvo_departure_monitor(**stop_info_config.__dict__)

        header_info = SIHeaderInfo(
            stop_data.get("Name",""),
            stop_data.get("Place",""),
            stop_data.get("ExpirationTime",None),
        )
        header.fill_header_info(header_info)

        for dep in stop_data['Departures']:

            direction = dep.get("Direction", "")
            mode_inf = MotInfo(dep.get("Mot", ""))
            scheduled = utils.VvoTime.from_string(dep["ScheduledTime"])
            state = VehicleState(dep.get("State", "none"))
            rt_s = dep.get("RealTime", None)
            if rt_s:
                real_time = utils.VvoTime.from_string(rt_s)
            else:
                real_time = scheduled
            plf = dep.get("Platform")
            if plf:
                new_plat = Platform(name=plf.get("Name", ""), type=plf.get("Type", ""))
            else: new_plat = Platform(name="no", type="data")

            card_data = CardData()

            card_data.tid       = dep.get("Id", "")
            card_data.line      = dep.get("LineName", "")
            card_data.direction = f"{mode_inf.icon} {direction}"
            card_data.scheduled = scheduled.format_6digits()
            card_data.real_time = real_time.diff_to_now()
            card_data.state     = state.clean_state
            card_data.platform  = f"{new_plat.type}: {new_plat.name}"
            card_data.mode      = mode_inf.clean_mot
            card_data.occupancy = dep.get("Occupancy", "Unknown")

            new_card = TramCardBig(card_data)
            content.mount(new_card)
            new_card.query_one(".state",Label).add_class(state.delay_status)
            new_card.query_one(".realtime",Label).add_class(state.delay_status)
            new_card.query_one("Digits",Digits).add_class(mode_inf.raw_mot)
            self.widgets_disp.append(new_card)

        #Logging Stuuff
        logger.write(stop_info_config)
        logger.write(header_info)


    def sort_depas(self, departures)->dict:
        depa_grouped = {}
        for departure in departures:
            depa_key = departure['Id']
            if depa_key not in depa_grouped:
                depa_grouped[depa_key] = []
            depa_grouped[depa_key].append(departure)
        return depa_grouped



class StopInfoContent(Container):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="SICScroller")


class StopInfoHeader_V3(Container):
    stop_place = reactive("")
    stop_name = reactive("")
    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.stop_name = "[i][b]stop-name[/b][/i]"
        self.stop_place = "[i]city[/i]"
    def render(self):
        self.query_one("#disp-place", Static).update(self.stop_place)
        self.query_one("#disp-name", Static).update(self.stop_name)
        return super().render()

    def compose(self) -> ComposeResult:
        yield Input(
            id="stop-info-text-input",
            placeholder="Enter a stop",
            validators=[Length(minimum=3, maximum=None, failure_description="min 3 char")],
            )
        yield Button("\nrfrsh", id="button-refresh", variant="success")
        yield Button("\nclear", id="button-clear", variant="primary")
        #yield Static(classes="err alt", id="disp-err")
        yield Static(classes="place", id="disp-place")
        yield Static("󰰂",classes="icon", id="disp-icon")
        yield Static(classes="name", id="disp-name")
        #yield Static(classes="time alt", id="disp-exp")

    def fill_header_info(self, header_info):
        if header_info.stop_place == "Dresden":
            header_info.stop_place = "DD"
        self.stop_place = header_info.stop_place
        self.stop_name = header_info.stop_name

    def clear_header_info(self):
        self.stop_name = "[i][b]stop-name[/b][/i]"
        self.stop_place = "[i]city[/i]"

    def read_config_change(self, settings):
        self.settings = settings
        self.conf_poif_stops_only = settings['stops-only']
        self.conf_poif_regional_only = settings['regional-only']
        self.conf_poif_stop_shortcuts = settings['stop-shortcuts']
        self.app.query_one("#log1_content", RichLog).write(settings)
