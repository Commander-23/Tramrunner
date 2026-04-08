from textual import on

from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.reactive import reactive
from textual.validation import Length
from textual.containers import Container, VerticalScroll
from textual.widgets import Button, Input, Static, Digits, RichLog, DataTable, Switch
from textual.widgets import Label, Placeholder, Collapsible, SelectionList, Pretty, RadioSet, RadioButton
import utils, api
from datetime import datetime
import pytz

class StopInfo(Container):
    def compose(self) -> ComposeResult:
        #yield StopInfoHeader_V2(id="header-v2")
        yield StopInfoHeader_V3(id="header-v3")
        yield StopInfoContent(id="content-v2")

    def test(self):
        content_box = self.query_one("#content-log", RichLog)
        query_config = {
            'stopid': utils.get_stop_id_from_pointfinder("rac"),
            'limit': 10,
            'time': '',
            'isarrival': False,
            'shorttermchanges': False,
            'mot': ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"]
        }
        stop_info_data = api.vvo_departure_monitor(**query_config)
        self.button_clear()
        self.get_data(stop_info_data)

        depa_grouped = self.sort_depas(stop_info_data['Departures'])
        for depa_dir in depa_grouped:
            new_thing = depa_grouped[depa_dir]
            info_line = f"{new_thing[0]['LineName']} - {depa_grouped[depa_dir][0]['Direction']}"
            info_count = f"{len(new_thing)}"
            content_box.write(info_line)
            content_box.write(info_count)

        table = self.query_one("#test-tt", DataTable)
        table.add_columns("Id", "Number", "Name")
        rows = []
        for key, group in depa_grouped.items():
            rows.append((f"[b]--- {key} ---[/b]", "", ""))
            for item in group:
                rows.append((
                    utils.diff_to_now(item["ScheduledTime"]),
                    item["LineName"],
                    item["Direction"]
                ))
        for row in rows:
            table.add_row(*row)
        self.sort_depas(stop_info_data['Departures'])

    def get_data(self, query_text):
        # assemble config and query departure monitor
        query_config = {
            'stopid': utils.get_stop_id_from_pointfinder(query_text),
            'limit': 20,
            'time': '',
            'isarrival': False,
            'shorttermchanges': False,
            'mot': ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train"]#, "Cableway", "Ferry", "HailedSharedTaxi"]
        }
        stop_data = api.vvo_departure_monitor(**query_config)

        depa_grouped = self.sort_depas(stop_data['Departures'])
        header = self.query_one("#header-v3", StopInfoHeader_V3)
        
        header.stop_name = stop_data['Name']
        header.stop_place = stop_data['Place']
        header.stop_expiry = utils.diff_to_now(stop_data['ExpirationTime'])

        self.app.query_one("#content-log", RichLog).write(stop_data)

    def sort_depas(self, departures)->dict:
        depa_grouped = {}
        for departure in departures:
            depa_key = departure['Id']
            if depa_key not in depa_grouped:
                depa_grouped[depa_key] = []
            depa_grouped[depa_key].append(departure)
        return depa_grouped

