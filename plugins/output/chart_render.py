from core.protocols import DataSink
from typing import List,Dict
from .dashboard import *
from .prompt_handler import *

class ChartWriter(DataSink):
    def write(self, records,config:Dict,filtered_data,reshaped_data) -> None:
        self.config = config
        show_dashboard(config,filtered_data,records,reshaped_data)

