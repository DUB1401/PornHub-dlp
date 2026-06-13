from enum import Enum

class Qualities(Enum):
	"""Перечисление разрешений видео."""

	_4K = 2160
	_2K = 1440
	_FullHD = 1080
	_HD = 720
	_480p = 480
	_360p = 360
	_240p = 240