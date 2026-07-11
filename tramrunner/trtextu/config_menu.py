from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, SelectionList, Switch, Static, Digits, RichLog

from copy import deepcopy
from datetime import datetime, time

class Configurator(Container):
    def compose(self) -> ComposeResult:
        with Container(classes="configCont"):
            with Container(id="config-save-quit", classes="wqbuttons"):
                yield Button("Exit", disabled=False, id="button-conf-exit", variant="error")
                yield Button("Save", disabled=False, id="button-conf-save", variant="success")
            with VerticalScroll(id="config-modal", classes="conf-stop-finder"):
                yield SwitchList([
                    {"id":"stops-only"    ,"value":True  ,"label":"stops-only"},
                    {"id":"regional-only" ,"value":False ,"label":"regional-only"},
                    {"id":"stop-shortcuts","value":False ,"label":"stop-shortcuts"},
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

    def load_config(self):
        self.edit_config = deepcopy(self.app.config)
        
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


# Config Components


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

class PointFinderConfig(Container):
    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True, limit = 1, stopsOnly = False, regionalOnly = False, stopShortcuts = False):
        self.limit: int = limit
        self.stopsOnly: bool = stopsOnly
        self.regionalOnly: bool = regionalOnly
        self.stopShortcuts: bool = stopShortcuts
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
    def compose(self) -> ComposeResult:
        yield
