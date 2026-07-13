from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, SelectionList, Switch, Static, Digits, RichLog, Label
from .daclas import *
from copy import deepcopy
from datetime import datetime, time

class Configurator(Container):
    def __init__(self, config: AppConfig, **kwargs):
        self.edit_config: AppConfig = deepcopy(config)
        super().__init__(**kwargs)
    def compose(self) -> ComposeResult:
        with Container(id="config-save-quit", classes="wqbuttons"):
            yield Button("Save", disabled=False, id="button-conf-save", variant="success")
            yield Button("Exit", disabled=False, id="button-conf-exit", variant="error")
        yield PointFinderConfWdgt(config=self.edit_config, id="pointfinderconf", classes="pointfinder-conf")
        yield StopInfoConfWdgt(config=self.edit_config, id="stopinfoconf", classes="stopinfo-conf",)

    def load_config(self):
        self.edit_config = deepcopy(self.app.config)

    @on(Button.Pressed, "#button-conf-save")
    def button_conf_save(self, event):
        self.app.config = deepcopy(self.edit_config)
        logger = self.app.query_one("#log1_content", RichLog)
        logger.write(self.edit_config)

    @on(Button.Pressed, "#button-conf-exit")
    def button_conf_exit(self, event):
        self.edit_config = deepcopy(self.app.config)



# Config Components
class PointFinderConfWdgt(Container):
    def __init__(self, config: AppConfig, **kwargs):
            self.config = config
            super().__init__(**kwargs)
    def compose(self) -> ComposeResult:
        self.border_title = "Pointfinder configuration Options"
        yield LimitPicker(
            setup={"title": "Limit", "text": "poi Results"},
            value = self.config.pointFinder.limit,
            id="limit1")
        yield SwitchList([
                {"id":"stops-only"    ,"value":True  ,"label":"stops-only"},
                {"id":"regional-only" ,"value":False ,"label":"regional-only"},
                {"id":"stop-shortcuts","value":False ,"label":"stop-shortcuts"},
            ])
    def on_mount(self):
        picker = self.query_one("#limit1",LimitPicker)
        self.watch(picker, "limit", self._limit_changed)
    def _limit_changed(self, old_value, new_value):
        self.app.query_one("#log1_content", RichLog).write("chenge claees")
        self.config.pointFinder.limit = new_value

class StopInfoConfWdgt(Container):
    def __init__(self, config: AppConfig, **kwargs):
        super().__init__(**kwargs)
        self.config = config
    def compose(self) -> ComposeResult:
        self.border_title = "Stop info configuration Options"
        yield LimitPicker(
            setup={"title": "Limit", "text": "stop Results"},
            value = self.config.stopInfo.limit,
            id="limit2")
        yield TimePicker()
        yield SwitchList([
                {"id":"isarrival"    ,"value":False  ,"label":"isarrival"},
                {"id":"shorttermchanges" ,"value":False ,"label":"shorttermchanges"},
            ])
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
    def on_mount(self):
        picker = self.query_one("#limit2",LimitPicker)
        self.watch(picker, "limit", self._limit_changed)
    def _limit_changed(self, old, value):
        self.config.stopInfo.limit = value

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
    number = reactive(0)
    def __init__(self, config, initval=0,**kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.number = initval
    def compose(self) -> ComposeResult:
        with Container(classes="entry"):
            yield Button("+1", compact=self.config["small-buttons"], classes="plus")
            yield Digits(self.digits, id="digitz")
            yield Button("-1", compact=self.config["small-buttons"], classes="minus")
    def watch_number(self, new):
        print("NumberClicker", self.id, repr(new), type(new))
        if self.is_mounted:
            self.query_one(Digits).update(self.digits)
    @property
    def digits(self):
        return f"{self.number:02d}"
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
        self.border_title="Select Time"
        #with HorizontalGroup(classes="tp-cont"):
        yield NumberClicker({"small-buttons": True, "min": 0, "max": 23})#.data_bind(number=TimePicker.hours)
        yield NumberClicker({"small-buttons": True, "min": 0, "max": 59})#.data_bind(number=TimePicker.minutes)
        yield NumberClicker({"small-buttons": True, "min": 0, "max": 59})#.data_bind(number=TimePicker.seconds)
        #with HorizontalGroup(classes="tp-butts-grp"):
        yield Button("Now", classes="tp-butts", id="tp-button-now", disabled=True)
        yield Button("+15", classes="tp-butts", id="tp-button-p15", disabled=True)
        yield Button("+30", classes="tp-butts", id="tp-button-p30", disabled=True)
    def compute_settime(self) -> datetime:
        return time(hour=self.hours, minute=self.minutes, second=self.seconds)

class LimitPicker(Container):
    limit = reactive(0, init=True)
    def __init__(self, setup, value=0, **kwargs):
        super().__init__(**kwargs)
        self.setup = setup
        self.limit = value
        self.inival = value
    def compose(self) -> ComposeResult:
        self.border_title=self.setup["title"]
        self.clicker = NumberClicker({"small-buttons": True, "min": 0, "max": 99}, self.limit)
        self.clicker.number = self.inival
        yield Static(self.setup["text"])
        yield self.clicker
    def on_mount(self):
        self.watch(self.clicker, "number", self.number_changed)
        self.clicker.number = self.limit

    def number_changed(self, old, value):
        print(self.id, old, value)
        self.limit = value