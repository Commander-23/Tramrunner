from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, SelectionList, Switch, Static, Digits, RichLog, Label
from .daclas import *
from copy import deepcopy
from datetime import datetime, time
import utils





_CONFIG_REGISTRY: dict[str, type] = {}

def config_section(name: str):
    """Decorator: registers a dataclass as a config section."""
    def wrapper(cls):
        _CONFIG_REGISTRY[name] = cls
        return cls
    return wrapper

@config_section("pointFinder")
@dataclass
class PointFinderConfig:
    limit:         int  = 5
    stopsOnly:     bool = True
    regionalOnly:  bool = True
    stopShortcuts: bool = False

@config_section("stopInfo")
@dataclass
class StopInfoConfig:
    limit:            int  = 20
    useNow:           bool = True   # query with the current time instead of `time`
    time:             str  = ""     # fixed time "HH:MM:SS", used when useNow is off
    isarrival:        bool = False
    shorttermchanges: bool = False
    mot:              list = field(default_factory=lambda: ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train"])

# (label, VVO mot name) for the means-of-transport selector
MOT_OPTIONS: list[tuple[str, str]] = [
    ("󰿧 Tram ", "Tram"),
    ("󰃧 Bus  ", "CityBus"),
    ("󰃧 ICBus", "IntercityBus"),
    (" Bahn ", "SuburbanRailway"),
    ("󰣄 Zug  ", "Train"),
    (" SSB  ", "Cableway"),
    ("󰈓 Fähr ", "Ferry"),
    ("󰓿 taxi ", "HailedSharedTaxi"),
]

class AppConfig:
    """Holds one instance per registered section, built from defaults."""
    def __init__(self):
        for name, cls in _CONFIG_REGISTRY.items():
            setattr(self, name, cls())

    def to_dict(self) -> dict:
        return {name: asdict(getattr(self, name)) for name in _CONFIG_REGISTRY}

    def load_dict(self, data: dict) -> None:
        for name, cls in _CONFIG_REGISTRY.items():
            if name in data:
                setattr(self, name, cls(**data[name]))

















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

    def read_widgets(self) -> AppConfig:
        """Build a new AppConfig from the current widget values."""
        config = deepcopy(self.app.config)

        pf = config.pointFinder
        pf.limit         = self.query_one("#limit1", LimitPicker).limit
        pf.stopsOnly     = self.query_one("#stops-only", Switch).value
        pf.regionalOnly  = self.query_one("#regional-only", Switch).value
        pf.stopShortcuts = self.query_one("#stop-shortcuts", Switch).value

        si = config.stopInfo
        si.limit            = self.query_one("#limit2", LimitPicker).limit
        picker = self.query_one("#timepicker", TimePicker)
        si.useNow           = picker.use_now
        si.time             = picker.time_value
        si.isarrival        = self.query_one("#isarrival", Switch).value
        si.shorttermchanges = self.query_one("#shorttermchanges", Switch).value
        selected = self.query_one("#mot-selector", SelectionList).selected
        si.mot = [mot for _, mot in MOT_OPTIONS if mot in selected]
        return config

    def load_widgets(self, config: AppConfig) -> None:
        """Push the values of `config` into the widgets."""
        pf = config.pointFinder
        self.query_one("#limit1", LimitPicker).limit      = pf.limit
        self.query_one("#stops-only", Switch).value       = pf.stopsOnly
        self.query_one("#regional-only", Switch).value    = pf.regionalOnly
        self.query_one("#stop-shortcuts", Switch).value   = pf.stopShortcuts

        si = config.stopInfo
        self.query_one("#limit2", LimitPicker).limit      = si.limit
        picker = self.query_one("#timepicker", TimePicker)
        picker.set_time(si.time)
        picker.use_now = si.useNow
        self.query_one("#isarrival", Switch).value        = si.isarrival
        self.query_one("#shorttermchanges", Switch).value = si.shorttermchanges
        selector = self.query_one("#mot-selector", SelectionList)
        selector.deselect_all()
        for mot in si.mot:
            selector.select(mot)

    @on(Button.Pressed, "#button-conf-save")
    def button_conf_save(self, event):
        self.edit_config = self.read_widgets()
        self.app.config = deepcopy(self.edit_config)
        logger = self.app.query_one("#log1_content", RichLog)
        logger.write(self.edit_config)

    @on(Button.Pressed, "#button-conf-exit")
    def button_conf_exit(self, event):
        """Discard unsaved edits and reset the widgets to the saved config."""
        self.edit_config = deepcopy(self.app.config)
        self.load_widgets(self.edit_config)


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
                {"id":"stops-only"    ,"value":self.config.pointFinder.stopsOnly  ,"label":"stops-only"},
                {"id":"regional-only" ,"value":self.config.pointFinder.regionalOnly ,"label":"regional-only"},
                {"id":"stop-shortcuts","value":self.config.pointFinder.stopShortcuts ,"label":"stop-shortcuts"},
            ])

class StopInfoConfWdgt(Container):
    def __init__(self, config: AppConfig, **kwargs):
        self.config = config
        super().__init__(**kwargs)
    def compose(self) -> ComposeResult:
        self.border_title = "Stop info configuration Options"
        yield LimitPicker(
            setup={"title": "Limit", "text": "stop Results"},
            value = self.config.stopInfo.limit,
            id="limit2")
        yield TimePicker(value=self.config.stopInfo.time, use_now=self.config.stopInfo.useNow, id="timepicker")
        yield SwitchList([
                {"id":"isarrival"        ,"value":self.config.stopInfo.isarrival        ,"label":"isarrival"},
                {"id":"shorttermchanges" ,"value":self.config.stopInfo.shorttermchanges ,"label":"shorttermchanges"},
            ])
        with Container(id="conf-mot"):
                yield SelectionList[str](
                    *[(label, mot, mot in self.config.stopInfo.mot) for label, mot in MOT_OPTIONS],
                    id="mot-selector",
                )

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
    """Pick a fixed time of day, or follow the current time after pressing "Now"."""
    def __init__(self, value: str = "", use_now: bool = True, **kwargs):
        super().__init__(**kwargs)
        self._initial = self._parse(value)
        self._use_now = use_now
        self._setting_time = False

    @staticmethod
    def _parse(value: str) -> tuple[int, int, int]:
        if not value:
            return (0, 0, 0)
        try:
            t = time.fromisoformat(value)
        except ValueError:
            return (0, 0, 0)
        return (t.hour, t.minute, t.second)

    def compose(self) -> ComposeResult:
        self.border_title="Select Time"
        h, m, s = self._initial
        yield NumberClicker({"small-buttons": True, "min": 0, "max": 23}, h, id="tp-hours")
        yield NumberClicker({"small-buttons": True, "min": 0, "max": 59}, m, id="tp-minutes")
        yield NumberClicker({"small-buttons": True, "min": 0, "max": 59}, s, id="tp-seconds")
        yield Button("Now", classes="tp-butts", id="tp-button-now")
        yield Button("+15", classes="tp-butts", id="tp-button-p15", disabled=True)
        yield Button("+30", classes="tp-butts", id="tp-button-p30", disabled=True)

    def on_mount(self):
        if self._use_now:
            self.set_now()
        for clicker in self.query(NumberClicker):
            self.watch(clicker, "number", self._time_changed, init=False)

    @property
    def use_now(self) -> bool:
        return self._use_now

    @use_now.setter
    def use_now(self, value: bool) -> None:
        self._use_now = value

    @property
    def time_value(self) -> str:
        """The time shown in the picker as "HH:MM:SS"."""
        h = self.query_one("#tp-hours", NumberClicker).number
        m = self.query_one("#tp-minutes", NumberClicker).number
        s = self.query_one("#tp-seconds", NumberClicker).number
        return time(hour=h, minute=m, second=s).isoformat()

    def set_time(self, value: str) -> None:
        h, m, s = self._parse(value)
        self._setting_time = True
        try:
            self.query_one("#tp-hours", NumberClicker).number = h
            self.query_one("#tp-minutes", NumberClicker).number = m
            self.query_one("#tp-seconds", NumberClicker).number = s
        finally:
            self._setting_time = False

    def set_now(self) -> None:
        """Show the current (Dresden) time."""
        self.set_time(utils.vvo_now().time().isoformat())

    @on(Button.Pressed, "#tp-button-now")
    def now_pressed(self):
        self._use_now = True
        self.set_now()

    def _time_changed(self, old_value, new_value):
        if not self._setting_time:
            self._use_now = False

class LimitPicker(Container):
    limit = reactive(0)
    def __init__(self, setup, value=0, **kwargs):
        self.clicker: NumberClicker | None = None
        super().__init__(**kwargs)
        self.setup = setup
        self.limit = value
    def compose(self) -> ComposeResult:
        self.border_title=self.setup["title"]
        self.clicker = NumberClicker({"small-buttons": True, "min": 0, "max": 99}, self.limit)
        yield Static(self.setup["text"])
        yield self.clicker
    def on_mount(self):
        self.watch(self.clicker, "number", self.number_changed)
        self.clicker.number = self.limit

    def watch_limit(self, value):
        # keep the clicker in sync when limit is set from outside (e.g. Exit/reset)
        if self.clicker is not None:
            self.clicker.number = value

    def number_changed(self, old, value):
        self.limit = value
