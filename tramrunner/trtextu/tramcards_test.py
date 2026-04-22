from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane, Input, RichLog, Button, Digits,Label, Placeholder
from textual.containers import Container, Grid, VerticalScroll, Vertical, VerticalGroup
from textual.validation import Validator, ValidationResult

sample_data = [
        {
            "Id": "voe:11008: :H:j26",
            "DlId": "de:vvo:11-8",
            "LineName": "8",
            "Direction": "Südvorstadt",
            "Platform": {"Name": "4","Type": "Platform"},
            "Mot": "Tram",
            "RealTime": "/Date(1776843720000-0000)/",
            "ScheduledTime": "/Date(1776843720000-0000)/",
            "State": "InTime",
            "RouteChanges": [],
            "Diva": {"Number": "11008","Network": "voe"},
            "CancelReasons": [],
            "Occupancy": "Unknown"
        },
        {
            "Id": "voe:11007: :H:j26",
            "DlId": "de:vvo:11-7",
            "LineName": "7",
            "Direction": "Pennrich",
            "Platform": {
                "Name": "2",
                "Type": "Platform"
            },
            "Mot": "Tram",
            "RealTime": "/Date(1776843720000-0000)/",
            "ScheduledTime": "/Date(1776843720000-0000)/",
            "State": "InTime",
            "RouteChanges": [],
            "Diva": {
                "Number": "11007",
                "Network": "voe"
            },
            "CancelReasons": [],
            "Occupancy": "Unknown"
        },
        {
            "Id": "ddb:87D03:C:H:j26",
            "DlId": "",
            "LineName": "SEV",
            "Direction": "S-Bahnhof Plauen",
            "Mot": "IntercityBus",
            "ScheduledTime": "/Date(1776843780000-0000)/",
            "RouteChanges": [],
            "Diva": {
                "Number": "87D03C",
                "Network": "ddb"
            },
            "CancelReasons": [],
            "Occupancy": "Unknown"
        },
        {
            "Id": "voe:23360: :R:j26",
            "DlId": "de:vvo:23-360",
            "LineName": "360",
            "Direction": "Pirnaischer Platz",
            "Platform": {
                "Name": "5",
                "Type": "Platform"
            },
            "Mot": "PlusBus",
            "RealTime": "/Date(1776843840000-0000)/",
            "ScheduledTime": "/Date(1776843540000-0000)/",
            "State": "Delayed",
            "RouteChanges": [
                "23586"
            ],
            "Diva": {
                "Number": "23360",
                "Network": "voe"
            },
            "CancelReasons": [],
            "Occupancy": "Unknown"
        },
        {
            "Id": "voe:11007: :R:j26",
            "DlId": "de:vvo:11-7",
            "LineName": "7",
            "Direction": "Weixdorf",
            "Platform": {
                "Name": "1",
                "Type": "Platform"
            },
            "Mot": "Tram",
            "RealTime": "/Date(1776843840000-0000)/",
            "ScheduledTime": "/Date(1776843780000-0000)/",
            "State": "Delayed",
            "RouteChanges": [],
            "Diva": {
                "Number": "11007",
                "Network": "voe"
            },
            "CancelReasons": [],
            "Occupancy": "StandingOnly"
        },
        {
            "Id": "voe:21066: :H:j26",
            "DlId": "de:vvo:21-66",
            "LineName": "66",
            "Direction": "Mockritz",
            "Platform": {
                "Name": "6",
                "Type": "Platform"
            },
            "Mot": "CityBus",
            "RealTime": "/Date(1776843900000-0000)/",
            "ScheduledTime": "/Date(1776843840000-0000)/",
            "State": "Delayed",
            "RouteChanges": [],
            "Diva": {
                "Number": "21066",
                "Network": "voe"
            },
            "CancelReasons": [],
            "Occupancy": "ManySeats"
        },
        {
            "Id": "voe:11010: :H:j26",
            "DlId": "de:vvo:11-10",
            "LineName": "10",
            "Direction": "MESSE DRESDEN",
            "Platform": {
                "Name": "2",
                "Type": "Platform"
            },
            "Mot": "Tram",
            "RealTime": "/Date(1776844020000-0000)/",
            "ScheduledTime": "/Date(1776843900000-0000)/",
            "State": "Delayed",
            "RouteChanges": [],
            "Diva": {
                "Number": "11010",
                "Network": "voe"
            },
            "CancelReasons": [],
            "Occupancy": "ManySeats"
        },
        {
            "Id": "voe:23333: :R:j26",
            "DlId": "de:vvo:23-333",
            "LineName": "333",
            "Direction": "Ammonstraße",
            "Platform": {
                "Name": "5",
                "Type": "Platform"
            },
            "Mot": "PlusBus",
            "RealTime": "/Date(1776844020000-0000)/",
            "ScheduledTime": "/Date(1776843960000-0000)/",
            "State": "Delayed",
            "RouteChanges": [
                "25558",
                "25375",
                "23971",
                "24199"
            ],
            "Diva": {
                "Number": "23333",
                "Network": "voe"
            },
            "CancelReasons": [],
            "Occupancy": "Unknown"
        },
        {
            "Id": "voe:21066: :R:j26",
            "DlId": "de:vvo:21-66",
            "LineName": "66",
            "Direction": "Nickern",
            "Platform": {
                "Name": "5",
                "Type": "Platform"
            },
            "Mot": "CityBus",
            "RealTime": "/Date(1776844020000-0000)/",
            "ScheduledTime": "/Date(1776844020000-0000)/",
            "State": "InTime",
            "RouteChanges": [],
            "Diva": {
                "Number": "21066",
                "Network": "voe"
            },
            "CancelReasons": [],
            "Occupancy": "Unknown"
        },
        {
            "Id": "voe:11003: :R:j26",
            "DlId": "de:vvo:11-3",
            "LineName": "3",
            "Direction": "Coschütz",
            "Platform": {
                "Name": "4",
                "Type": "Platform"
            },
            "Mot": "Tram",
            "RealTime": "/Date(1776844080000-0000)/",
            "ScheduledTime": "/Date(1776844020000-0000)/",
            "State": "Delayed",
            "RouteChanges": [],
            "Diva": {
                "Number": "11003",
                "Network": "voe"
            },
            "CancelReasons": [],
            "Occupancy": "ManySeats"
        }]

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
    def compose(self):
        self.border_title=self.val_dir
        with Grid():
            #yield Label(self.val_sep, classes="seperator")
            yield Digits(self.val_dig)

            yield Label(self.val_dir, classes="direction")
            yield Label(self.val_mot, classes="mot")
            yield Placeholder()

            yield Label(self.val_tli, classes="live-time")
            yield Label(self.val_plf, classes="platform")
            yield Placeholder()

            yield Label(self.val_del, classes="delayinf")
            yield Placeholder("0")
            yield Placeholder()

class TramCardsApp(App[None]):
    """We gonn make it"""
    #CSS_FILES = ["trtextu/css/header_v3.tcss","trtextu/css/loggerPane.tcss"]
    CSS_FILES = ["css/tramcards.tcss"]
    CSS_PATH = CSS_FILES
    def compose(self) -> ComposeResult:
        with VerticalScroll():
            self.add_new_wdg()
            #for item in sample_data:
            yield TramCardBig()


if __name__ == "__main__":
    app = TramCardsApp()
    app.run()