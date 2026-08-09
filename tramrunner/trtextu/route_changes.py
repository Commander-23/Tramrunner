from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, HorizontalGroup
from textual.widgets import Button, Input, Static, Digits, RichLog, DataTable, Switch
from textual.widgets import Label, Placeholder, Collapsible, SelectionList, Pretty, RadioSet, RadioButton
import api, utils
class RouteChanges(Container):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def compose(self) -> ComposeResult:
        self.logger = RichLog(id="route-changes-log", highlight=True, markup=True, auto_scroll=False)
        with HorizontalGroup(id="route-changes-buttons"):
            yield Button("Clear", id="route-changes-clear", variant="warning")
            yield Button("Print Lines", id="route-changes-print-lines", variant="primary")
            yield Button("Print Changes", id="route-changes-print-change", variant="primary")
            yield Button("Print Banners", id="route-changes-print-banners", disabled=True)
        with HorizontalGroup():
            self.lenbanners = Label("0", id="lenbanners", classes="rcvar")
            self.lenchanges = Label("0", id="lenchanges", classes="rcvar")
            self.lenlines = Label("0", id="lenlines", classes="rcvar")
            yield Label("Banners", classes="rclabel")
            yield self.lenbanners
            yield Label("Changes", classes="rclabel")
            yield self.lenchanges
            yield Label("Impacted lines", classes="rclabel")
            yield self.lenlines
        yield self.logger
        self.changedat = api.vvo_route_changes(False, "DVB")
        self.lenbanners.update(f"{len(self.changedat["Banners"])}")
        self.lenchanges.update(f"{len(self.changedat["Changes"])}")
        self.lenlines.update(f"{len(self.changedat["Lines"])}")

    @on(Button.Pressed, "#route-changes-clear")
    def clear_log(self):
        self.logger.clear()

    @on(Button.Pressed, "#route-changes-print-lines")
    def print_lines(self):
        self.logger.write(f"Lines Keys:   {self.changedat["Lines"][0].keys()}")
        for entry in self.changedat["Lines"]:
            self.logger.write(f"{entry["Name"]} {entry["RouteDescription"]}")

    @on(Button.Pressed, "#route-changes-print-change")
    def print_changes(self):
        self.logger.write(f"{self.changedat["Changes"][0].keys()}")
        for change in self.changedat["Changes"]:
            raw_start = utils.VvoTime.from_string(change["ValidityPeriods"][0]["Begin"])
            #raw_end = change["ValidityPeriods"][0]["End"]
            time_str = f"{raw_start.format_date()}"#{change["ValidityPeriods"][0]["Begin"]} - {change["ValidityPeriods"][0]["End"]}"
            self.logger.write(f"{time_str} {change["Title"]}  {change["LineIds"]}")

    @on(Button.Pressed, "#route-changes-print-banners")
    def print_banners(self):
        self.logger.write(f"Banners Keys: {self.changedat["Banners"][0].keys()}")
