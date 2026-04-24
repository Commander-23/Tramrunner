from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane, Input, RichLog, Button, Digits,Label, Placeholder
from textual.containers import Container, Grid, VerticalScroll, Vertical, VerticalGroup
from textual.validation import Validator, ValidationResult
from datetime import datetime


class TramCardBig(Container):
    val_sep = "---Header-Line---"
    val_dig = "99"
    val_mot = "tram"
    val_dir = " --> Kleinzschachwitz"
    val_plf = "Platform 1"
    val_tli = "live: 00:00"
    val_del = "Delayed"
    #tram color: tomato
    #bus color: steelblue
    def __init__(self, tid,line,direction,scheduled,real_time,state,platform,mode,occupancy, **kwargs):
        self.tid = tid
        self.line = line
        self.direction = direction
        self.scheduled = scheduled.strftime("%H:%M:%S")
        self.real_time = "None" #real_time.strftime("%H:%M:%S")
        self.state = state
        self.platform = "platform"
        self.mode = mode
        self.occupancy = occupancy
        #self.val_plf = f"{values.get('Platform').get('Type')} {values['Platform']['Name']}"
        super().__init__(**kwargs)


    def compose(self):
        self.border_title=self.direction
        with Grid():
            #yield Label(self.val_sep, classes="seperator")
            yield Digits(self.line)

            yield Label("Scheduled", classes="direction")
            yield Label(self.state, classes="mot")
            yield Placeholder()

            yield Label(self.scheduled, classes="live-time")
            yield Label(self.real_time, classes="platform")
            yield Placeholder()

            yield Label(self.state, classes="delayinf")
            yield Placeholder("0")
            yield Placeholder()
