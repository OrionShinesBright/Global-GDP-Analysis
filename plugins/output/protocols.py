from __future__ import annotations
from typing import List,Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from core.protocols import DataSink 

class OutputManager:

	def __init__(self,config: Dict):
		self.config = config
		self.sink = self._choose_sink()
		
	def _choose_sink(self) -> DataSink:
		output_type = self.config.get("output")
		
		if output_type == "console":
			from .console_writer import ConsoleWriter
			return ConsoleWriter()
			
		elif output_type == "chart":
			from .chart_render import ChartWriter
			return ChartWriter()
		else:
			raise ValueError(f"Unknown Output type : {output_type}")
	
	def get_sink(self) -> DataSink:
		return self.sink
