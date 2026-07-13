from dataclasses import dataclass, field
from typing import ClassVar
from datetime import datetime
import utils
import api, utils

@dataclass
class DepaMonConfig:
    stopid: str = field(init=False)
    limit: int
    time: any
    isarrival: bool
    shorttermchanges: bool
    mot: list

    @property
    def query_text(self):
        raise AttributeError("exestiert es nicht?!")

    @query_text.setter
    def query_text(self, query_usr_text):
        self.stopid = utils.get_stop_id_from_pointfinder(query_usr_text)

@dataclass
class SIHeaderInfo:
    stop_name: str
    stop_place: str
    expiration_time: datetime|str
    expiration_text: str = field(init=False)

    def __post_init__(self):
        if isinstance(self.expiration_time, str):
            self.expiration_time = utils.vvo_time_conv(self.expiration_time)
            self.expiration_text = utils.diff_to_now(self.expiration_time)

@dataclass
class CardData:
    tid: str = "tid"
    line: str = "line"
    direction: str = "dir"  # destination name
    scheduled: datetime = None
    real_time: datetime | None = None
    state: str = "state"  # real-time state, e.g. "InTime", "Delayed"
    platform: any = None
    mode: str = "none"
    occupancy: str = "Unknown"  # "Unknown", "ManySeats", "StandingOnly", "Full"

@dataclass(frozen=True, slots=True)
class Platform:
    """A platform or track at a stop."""

    name: str
    type: str  # "Platform" for bus/tram stops, "Railtrack" for train stations

@dataclass
class MotInfo:
    raw_mot: str
    clean_mot: str = ""
    icon: str = ""

    _lookup: ClassVar = {
        "Tram": {
            "clean_mot": "Tram",
            "icon": "󰿧",
        },
        "CityBus": {
            "clean_mot": "Bus",
            "icon": "󰃧",
        },
        "PlusBus": {
            "clean_mot": "PlusBus",
            "icon": "󰃧",
        },
        "IntercityBus": {
            "clean_mot": "ICBus",
            "icon": "󰃧",
        },
        "SuburbanRailway": {
            "clean_mot": "SBahn",
            "icon": "",
        },
        "Train": {
            "clean_mot": "Zug",
            "icon": "󰣄",
        },
        "Cableway": {
            "clean_mot": "blah",
            "icon": "",
        },
        "Ferry": {
            "clean_mot": "Fähre",
            "icon": "󰈓",
        },
        "HailedSharedTaxi": {
            "clean_mot": "Taxi",
            "icon": "󰓿",
        },
    }

    def __post_init__(self):
        if self.raw_mot in self._lookup:
            values = self._lookup[self.raw_mot]
            self.clean_mot = values["clean_mot"]
            self.icon = values["icon"]

@dataclass
class VehicleState:
    raw_state: str 
    clean_state: str = ""
    delay_status: str = ""

    _lookup: ClassVar = {
        "InTime": {
            "clean_state": "Pünktlich",
            "delay_status": "good",
        },
        "Delayed": {
            "clean_state": "Verspätet",
            "delay_status": "bad",
        },
    }
    def __post_init__(self):
            if self.raw_state in self._lookup:
                values = self._lookup[self.raw_state]
                self.clean_state = values["clean_state"]
                self.delay_status = values["delay_status"]
            else:
                self.clean_state = "nüscht"
                self.delay_status = "none"

@dataclass
class AppConfig:
    pointFinder: PointFinderConfig
    stopInfo: StopInfoConfig

@dataclass
class PointFinderConfig:
    limit:         int  = 5
    stopsOnly:     bool = True
    regionalOnly:  bool = True
    stopShortcuts: bool = False

@dataclass
class StopInfoConfig:
    limit:            int  = 20
    time:             any  = ""
    isarrival:        bool = False
    shorttermchanges: bool = False
    mot:              list = field(default_factory=lambda: ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"])