from dublib.Methods.Filesystem import ListDir
from pathlib import Path

class Driver:
	"""Драйвер обработчиков источников."""

	@property
	def processors_names(self) -> tuple[str, ...]:
		"""Последовательность имён обработчиков."""

		ProcessorsDirectory = Path("Source/Processors")
		if not ProcessorsDirectory.exists(): return tuple()

		return tuple(ListDir(ProcessorsDirectory))