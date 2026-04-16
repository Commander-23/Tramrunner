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