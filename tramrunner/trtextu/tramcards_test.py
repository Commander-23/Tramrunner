from textual.widgets import Digits,Label, Placeholder
from textual.containers import Container, Grid
from datetime import datetime
from dataclasses import dataclass


class TramCardBig(Container):
    #tram color: tomato
    #bus color: steelblue
    def __init__(self, tid,line,direction,scheduled,real_time,state,platform,mode,occupancy, **kwargs):
        self.tid = tid
        self.line = line
        self.direction = direction
        self.scheduled = scheduled#.strftime("%H:%M:%S")
        self.real_time = real_time 
        self.state = state
        self.platform = platform
        self.mode = mode
        self.occupancy = occupancy
        #self.val_plf = f"{values.get('Platform').get('Type')} {values['Platform']['Name']}"
        super().__init__(**kwargs)


    def compose(self):
        self.border_title=self.direction
        with Grid():
            #yield Label(self.val_sep, classes="seperator")
            yield Digits(self.line)

            yield Label(self.mode, classes="direction")
            yield Label(self.platform, classes="mot")
            yield Placeholder()

            yield Label(self.scheduled, classes="live-time")
            yield Label(self.state, classes="platform")
            yield Placeholder()

            yield Label(self.real_time, classes="delayinf")
            yield Placeholder("0")
            yield Placeholder()

@dataclass
class CardData:
    tid: str
    line: str
    direction: str  # destination name
    scheduled: datetime
    real_time: datetime | None = None
    state: str = ""  # real-time state, e.g. "InTime", "Delayed"
    platform: Platform | None = None
    mode: str = ""  # e.g. "Tram", "CityBus", "SuburbanRailway", "Ferry"
    occupancy: str = "Unknown"  # "Unknown", "ManySeats", "StandingOnly", "Full"

    def __post_init__(self):
        pass

@dataclass(frozen=True, slots=True)
class Platform:
    """A platform or track at a stop."""

    name: str
    type: str  # "Platform" for bus/tram stops, "Railtrack" for train stations

