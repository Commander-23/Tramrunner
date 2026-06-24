from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.reactive import reactive
from textual.validation import Length
from textual.containers import Container, VerticalScroll, Horizontal, HorizontalGroup
from textual.widgets import Button, Input, Static, Digits, RichLog, DataTable, Switch
from textual.widgets import Label, Placeholder, Collapsible, SelectionList, Pretty, RadioSet, RadioButton

from .daclas import DepaMonConfig, SIHeaderInfo
from dataclasses import asdict
import utils, api
from datetime import datetime, time
import pytz
from .tramcards_test import CardData, Platform, TramCardBig

class StopInfo(Container):
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

    def test(self):
        query_text_val = self.query_one("#stop-info-text-input", Input).value
        content_box = self.parent.parent.query_one("#log1_content", RichLog)
        
        # TODO pull this info from the config Modal Screen
        query_config = {
            'stopid': utils.get_stop_id_from_pointfinder("rac"),
            'limit': 10,
            'time': '',
            'isarrival': False,
            'shorttermchanges': False,
            'mot': ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"]
        }
        stop_info_data = api.vvo_departure_monitor(**query_config)
        self.get_data(stop_info_data)

        depa_grouped = self.sort_depas(stop_info_data['Departures'])
        for depa_dir in depa_grouped:
            new_thing = depa_grouped[depa_dir]
            info_line = f"{new_thing[0]['LineName']} - {depa_grouped[depa_dir][0]['Direction']}"
            info_count = f"{len(new_thing)}"
            content_box.write(info_line)
            content_box.write(info_count)

        #table = self.query_one("#test-tt", DataTable)
        #table.add_columns("Id", "Number", "Name")
        #rows = []
        #for key, group in depa_grouped.items():
        #    rows.append((f"[b]--- {key} ---[/b]", "", ""))
        #    for item in group:
        #        rows.append((
        #            utils.diff_to_now(item["ScheduledTime"]),
        #            item["LineName"],
        #            item["Direction"]
        #        ))
        #for row in rows:
        #    table.add_row(*row)
        #self.sort_depas(stop_info_data['Departures'])

    @on(Button.Pressed, "#button-refresh")
    @on(Input.Submitted, "#stop-info-text-input")
    def process_search_input(self):
        logger = self.app.query_one("#log1_content", RichLog)
        header = self.query_one("#header-v3", StopInfoHeader_V3)
        self.stop_info_config.query_text = self.query_one("#stop-info-text-input", Input).value
        stop_data = api.vvo_departure_monitor(**asdict(self.stop_info_config))
        content = self.parent.query_one("#SICScroller", VerticalScroll)

        header_info = SIHeaderInfo(
            stop_data['Name'],
            stop_data['Place'],
            stop_data["ExpirationTime"]
        )
        header.fill_header_info(header_info)
        
        for dep in stop_data['Departures']:
            logger.write(dep)
            scheduled = utils.vvo_time_conv(dep["ScheduledTime"]).strftime("%H:%M:%S")
            rt_s = dep.get("RealTime", None)
            if not rt_s:
                real_time = "None"
            else:
                try:
                    real_time = utils.vvo_time_conv(rt_s).strftime("%H:%M:%S")
                except ValueError:
                    real_time = "None"
            plf = dep.get("Platform")
            if plf:
                new_plat = Platform(name=plf.get("Name", ""), type=plf.get("Type", ""))
            else: new_plat = Platform(name="no", type="data")
            content.mount(TramCardBig(**asdict(CardData(
                        tid       = dep.get("Id", ""),
                        line      = dep.get("LineName", ""),
                        direction = dep.get("Direction", ""),
                        scheduled = scheduled,
                        real_time = real_time,
                        state     = dep.get("State", ""),
                        platform  = f"{new_plat.type}: {new_plat.name}",
                        mode      = dep.get("Mot", ""),
                        occupancy = dep.get("Occupancy", "Unknown"),
            ))))
            #yield TramCardBig(    
            #    tid        = 1, #dep.get("Id", ""),
            #    line       = 2, #dep.get("LineName", ""),
            #    direction  = 3, #dep.get("Direction", ""),
            #    scheduled  = 4, #scheduled,
            #    real_time  = 5, #real_time,
            #    state      = 6, #dep.get("State", ""),
            #    platform   = 7, #new_plat,
            #    mode       = 8, #dep.get("Mot", ""),
            #    occupancy  = 9, #dep.get("Occupancy", "Unknown"),
            #)
        
        #Logging Stuuff
        logger.write(self.stop_info_config)
        logger.write(header_info)
        #logger.write(stop_data)

#
#            tid=dep.get("Id", ""),
#            line=dep.get("LineName", ""),
#            direction=dep.get("Direction", ""),
#            state=dep.get("State", ""),
#            mode=dep.get("Mot", ""),
#            occupancy=dep.get("Occupancy", "Unknown"),
#            logger.write(tid)
#            logger.write(line)
#            logger.write(direction)
#            logger.write(state)
#            logger.write(mode)
#            logger.write(occupancy)
#            #yield TramCardBig(    
            #    tid=dep.get("Id", ""),
            #    line=dep.get("LineName", ""),
            #    direction=dep.get("Direction", ""),
            #    #scheduled=scheduled,
            #    #real_time=real_time,
            #    state=dep.get("State", ""),
            #    #platform=new_plat,
            #    mode=dep.get("Mot", ""),
            #    occupancy=dep.get("Occupancy", "Unknown"),
            #)


    def get_data(self, query_text):

        self.query_one("#header-v3", StopInfoHeader_V3).fill_header_info(header_info)
        
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
                **asdict(CardData(
                    tid=dep.get("Id", ""),
                    line=dep.get("LineName", ""),
                    direction=dep.get("Direction", ""),
                    scheduled=scheduled,
                    real_time=real_time,
                    state=dep.get("State", ""),
                    platform=new_plat,
                    mode=dep.get("Mot", ""),
                    occupancy=dep.get("Occupancy", "Unknown"),
                ))
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


class SiConfig(ModalScreen):
    def __init__(self, name = None, id = None, classes = None, stops_only = False, regional_only = False, stop_shortcuts = False):
        self.stops_only = stops_only
        self.regional_only = regional_only
        self.stop = stop_shortcuts
        super().__init__(name, id, classes)
    def compose(self) -> ComposeResult:
        with VerticalScroll(id="config-modal", classes="scroller"):
            with Container(id="config-save-quit", classes="wqbuttons"):
                yield Button("Exit", disabled=False, id="button-conf-exit", variant="error")
                yield Button("Save", disabled=False, id="button-conf-save", variant="success")
            with Container(classes="conf-stop-finder"):
                yield SwitchList([
                    {"id":"stops-only"    ,"value":self.stops_only   ,"label":"stops-only"},
                    {"id":"regional-only" ,"value":self.regional_only,"label":"regional-only"},
                    {"id":"stop-shortcuts","value":self.stop         ,"label":"stop-shortcuts"},
                ])
                yield TimePicker()
                yield NumberClicker({"small-buttons": True, "min": 0, "max": 99})   
                with Container(id="conf-mot"):                
                    yield SelectionList[int](  
                        ("󰿧 Tram ", 0, True),
                        ("󰃧 Bus  ", 1, True),
                        (" Bahn ", 2, True),
                        ("󰣄 Zug  ", 3, True),
                        (" SSB  ", 4, False),
                        ("󰈓 Fähr ", 5, False),
                        ("󰓿 taxi ", 6, False),
                        id="mot-selector",
                    )

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

class SwitchList(VerticalScroll):
    def __init__(self, config, **kwargs):
        self.config = config
        super().__init__(**kwargs) 
    def compose(self) -> ComposeResult:
        for item in self.config:
            with Container(classes="entry"):
                yield Switch(value=item["value"], animate=False, id=item["id"])
                yield Static(item["label"], classes="label")
class NumberClicker(Container):
    number = reactive(0, init=False)
    def __init__(self, config, **kwargs):
        self.config = config
        super().__init__(**kwargs)
    def compose(self) -> ComposeResult:
        with Container(classes="entry"):
            yield Button("+", compact=self.config["small-buttons"], classes="plus")
            yield Digits(self.digits, id="digitz")
            yield Button("-", compact=self.config["small-buttons"], classes="minus")
    def watch_number(self):
        self.query_one(Digits).update(self.digits)
        
    @property
    def digits(self):
        return "{:02d}".format(self.number)
    @on(Button.Pressed, ".plus")
    def add(self):
        d = self.number + 1
        if d > self.config["max"]: d = self.config["min"]
        self.number = d
    @on(Button.Pressed, ".minus")
    def substract(self):
        d = self.number - 1
        if d < self.config["min"]: d = self.config["max"]
        self.number = d
class TimePicker(Container):
    hours = reactive(0)
    minutes = reactive(0)
    seconds = reactive(0)
    settime: reactive[datetime] = reactive(time())
    def compose(self) -> ComposeResult:
        #with HorizontalGroup(classes="tp-cont"):
        yield NumberClicker({"small-buttons": True, "min": 0, "max": 23}).data_bind(number=TimePicker.hours)
        yield NumberClicker({"small-buttons": True, "min": 0, "max": 59}).data_bind(number=TimePicker.minutes)
        yield NumberClicker({"small-buttons": True, "min": 0, "max": 59}).data_bind(number=TimePicker.seconds)
        #with HorizontalGroup(classes="tp-butts-grp"):
        yield Button("Now", classes="tp-butts", id="tp-button-now")
        yield Button("+15", classes="tp-butts", id="tp-button-p15")
        yield Button("+30", classes="tp-butts", id="tp-button-p30")
    def compute_settime(self) -> datetime:
        return time(hour=self.hours, minute=self.minutes, second=self.seconds)
    def watch_settime(self, settime):
        self.app.query_one("#log1_content", RichLog).write(settime.strftime("%H:%M:%S1"))


class StopInfoContent(Container):
    def compose(self) -> ComposeResult:
        yield VerticalScroll(id="SICScroller")
        #yield Label("FYAD", id="fyad")
        #yield RichLog(id="content-log")
        #yield DataTable(id="test-tt")


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

    def fill_header_info(self, header_info):
        self.stop_name = header_info.stop_name
        self.stop_place = header_info.stop_place
        self.stop_expiry = header_info.expiration_text

    #@on(Input.Submitted, "#stop-info-text-input")
    

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
        self.app.query_one("#log1_content", RichLog).write(settings)

    @on(Input.Changed)
    def show_invalid_reasons(self, event: Input.Changed) -> None:
        # Updating the UI to show the reasons why validation failed
        if not event.validation_result.is_valid:  
           self.error_msg = str(event.validation_result.failure_descriptions)
        else:
            self.error_msg = ""