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
    stop_info_config = reactive(DepaMonConfig(
        #query_text="rac",
        limit=10,
        time ="",
        isarrival=False,
        shorttermchanges=False,
        mot=["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train"],#, "Cableway", "Ferry", "HailedSharedTaxi"]
        ))
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
        logger = self.app.query_one("#log1_content", RichLog)
        header = self.query_one("#header-v3", StopInfoHeader_V3)
        self.stop_info_config.query_text = self.query_one("#stop-info-text-input", Input).value
        stop_data = api.vvo_departure_monitor(**self.stop_info_config.__dict__)
        content = self.parent.query_one("#SICScroller", VerticalScroll)


        header_info = SIHeaderInfo(
            stop_data['Name'],
            stop_data['Place'],
            stop_data["ExpirationTime"]
        )
        header.fill_header_info(header_info)

        for dep in stop_data['Departures']:
            card_data = CardData()
            

            scheduled = utils.vvo_time_conv(dep["ScheduledTime"]).astimezone().strftime("%H:%M:%S")
            rt_s = dep.get("RealTime", None)
            if not rt_s:
                real_time = "None"
            else:
                try:
                    real_time = utils.vvo_time_conv(rt_s).astimezone().strftime("%H:%M:%S")
                except ValueError:
                    real_time = "None"
            plf = dep.get("Platform")
            if plf:
                new_plat = Platform(name=plf.get("Name", ""), type=plf.get("Type", ""))
            else: new_plat = Platform(name="no", type="data")

            card_data.tid = dep.get("Id", "")
            card_data.line = dep.get("LineName", "")
            card_data.direction = dep.get("Direction", "")
            card_data.scheduled = scheduled,
            card_data.real_time = real_time,
            card_data.state     = dep.get("State", ""),
            card_data.platform  = f"{new_plat.type}: {new_plat.name}",
            card_data.mode      = dep.get("Mot", ""),
            card_data.occupancy = dep.get("Occupancy", "Unknown"),
            new_card = TramCardBig(**card_data)
            new_card.add_class(dep.get("Mot", ""))
            content.mount(new_card)
            self.widgets_disp.append(new_card)

        #Logging Stuuff
        logger.write(self.stop_info_config)
        logger.write(header_info)


    def get_data(self, query_text):

        #self.query_one("#header-v3", StopInfoHeader_V3).fill_header_info(header_info)
        stop_data = None
        for dep in stop_data['Departures']:
            scheduled = utils.vvo_time_conv(dep["ScheduledTime"])
            rt_s = dep.get("RealTime", None)
            if not rt_s:
                real_time = None
            else:
                try:
                    real_time = utils.vvo_time_conv(rt_s)
                except ValueError:
                    real_time = None
            plf = dep.get("Platform")
            if plf:
                new_plat = Platform(name=plf.get("Name", ""), type=plf.get("Type", ""))
            else: Platform(name="", type="")
            yield TramCardBig(
                **CardData(
                    tid=dep.get("Id", ""),
                    line=dep.get("LineName", ""),
                    direction=dep.get("Direction", ""),
                    scheduled=scheduled,
                    real_time=real_time,
                    state=dep.get("State", ""),
                    platform=new_plat,
                    mode=dep.get("Mot", ""),
                    occupancy=dep.get("Occupancy", "Unknown"),
                ).__dict__
            )


        #self.app.query_one("#content-log", RichLog).write(stop_data)

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
    error_msg = reactive("")
    stop_place = reactive("")
    stop_name = reactive("")
    conf_poif_stops_only = reactive(False)
    conf_poif_regional_only = reactive(False)
    conf_poif_stop_shortcuts = reactive(False)
    settings = reactive([])
    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        self.stop_name = "[i][b]stop-name[/b][/i]"
        self.stop_place = "[i]city[/i]"
    def render(self):
        #self.query_one("#disp-err", Static).update(self.error_msg)
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
        yield Button("\nconf", id="button-conf-show", variant="primary")
        #yield Static(classes="err alt", id="disp-err")
        yield Static(classes="place", id="disp-place")
        yield Static("󰰂",classes="icon", id="disp-icon")
        yield Static(classes="name", id="disp-name")
        #yield Static(classes="time alt", id="disp-exp")

    def fill_header_info(self, header_info):
        dd = "DD"
        if header_info.stop_place == "Dresden":
            header_info.stop_place = "DD"

        self.stop_place = header_info.stop_place
        self.stop_name = header_info.stop_name

    def clear_header_info(self):
        self.stop_name = "[i][b]stop-name[/b][/i]"
        self.stop_place = "[i]city[/i]"


    @on(Button.Pressed, "#button-conf-show")
    def button_conf_show(self):
        logger = self.app.query_one("#log1_content", RichLog)
        logger.write(self.app.config)

    def read_config_change(self, settings):
        self.settings = settings
        self.conf_poif_stops_only = settings['stops-only']
        self.conf_poif_regional_only = settings['regional-only']
        self.conf_poif_stop_shortcuts = settings['stop-shortcuts']
        self.app.query_one("#log1_content", RichLog).write(settings)

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        if not event.validation_result.is_valid:  
           self.error_msg = str(event.validation_result.failure_descriptions)
        else:
            self.error_msg = ""