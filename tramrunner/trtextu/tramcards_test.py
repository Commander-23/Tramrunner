from textual.widgets import Digits,Label, Placeholder
from textual.containers import Container, Grid
from textual.reactive import reactive
from .daclas import CardData
class TramCardBig(Container):
    def __init__(self, card_dat: CardData, **kwargs):
        self.tid = card_dat.tid
        self.line = card_dat.line
        self.direction = card_dat.direction
        self.scheduled = card_dat.scheduled#.strftime("%H:%M:%S")
        self.real_time = card_dat.real_time 
        self.state = card_dat.state
        self.platform = card_dat.platform
        self.mode = card_dat.mode
        self.occupancy = card_dat.occupancy
        super().__init__(**kwargs)

    def compose(self):
        self.border_title=self.direction
        with Grid():
            yield Digits(self.line)

            yield Label(self.state, classes="time state")
            yield Label(self.platform)

            yield Label(self.scheduled, classes="time scheduled")
            yield Label(self.state, )

            yield Label(self.real_time, classes="time realtime")
            yield Label()

