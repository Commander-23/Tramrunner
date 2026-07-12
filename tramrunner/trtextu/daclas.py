from dataclasses import dataclass, field
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
    mode: str = "none"  # e.g. "Tram", "CityBus", "SuburbanRailway", "Ferry"
    occupancy: str = "Unknown"  # "Unknown", "ManySeats", "StandingOnly", "Full"

    def __post_init__(self):
        pass

@dataclass(frozen=True, slots=True)
class Platform:
    """A platform or track at a stop."""

    name: str
    type: str  # "Platform" for bus/tram stops, "Railtrack" for train stations


#@dataclass
#class StopInfoGather:
#    Id: str
##    DlId: str             # no need, can be assembled from LineName & id
#    LineName: int|str      # usually int sometimes str "8, 10, S8, S1"
#    Direction: str         # sometimes really long --> truncate
#    Platform: dict
#    Mot: str
#    RealTime: str
#    ScheduledTime: datetime | None = field(init=False)
#    State: str = ""
#    RouteChanges: list
#    CancelReasons: list
#    Occupancy: str = ""

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
    limit: int =10,
    time:         str|None = "",
    isarrival:        bool = False,
    shorttermchanges: bool = False,
    mot: list = ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train"],#, "Cableway", "Ferry", "HailedSharedTaxi"]