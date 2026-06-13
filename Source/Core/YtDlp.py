from .Enums import Qualities

from dublib.CLI.Validators import Validator_URL
from dublib.Methods.Data import ToSequence
from dublib.WebRequestor import Proxy

from typing import cast, TYPE_CHECKING
from pathlib import Path
from os import PathLike
import ssl

from yt_dlp.networking.impersonate import ImpersonateTarget
from yt_dlp.version import __version__
import yt_dlp

if TYPE_CHECKING:
	from yt_dlp import _Params

# Отключение проверки SSL.
ssl._create_default_https_context = ssl._create_unverified_context

class YtDlp:
	"""Оператор взаимодействий с **yt-dlp**."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def operator(self) -> yt_dlp.YoutubeDL:
		"""Оператор."""

		return self.__Operator

	@property
	def version(self) -> str:
		"""Версия **yt-dlp**."""

		return __version__

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __ReinitializeOperator(self) -> yt_dlp.YoutubeDL:
		"""
		Генерирует параметры **yt-dlp** на основе атрибутов объекта и реинициализирует оператор.

		:return: Оператор.
		:rtype: yt_dlp.YoutubeDL
		"""

		Parameters: dict = {
			"format": "bv*+ba/b",
			"format_sort": (f"res:{self.__Quality}", "ext:mp4:m4a"), 
			"outtmpl": self.__OutputDirectory.as_posix() + f"/{self.__FilenameTemplate}",
			"ignoreerrors": True,  
			"impersonate": ImpersonateTarget.from_str("chrome")
		}

		if self.__Proxy: Parameters["proxy"] = self.__Proxy.to_string()
		self.__Operator = yt_dlp.YoutubeDL(cast("_Params", Parameters))

		return self.__Operator

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Оператор взаимодействий с **yt-dlp**."""

		self.__FilenameTemplate = "%(title)s.%(ext)s"
		self.__OutputDirectory = Path("Downloads")
		self.__OutputDirectory.mkdir(exist_ok = True)
		self.__Proxy: Proxy | None = None
		self.__Quality: int = Qualities._FullHD.value

		self.__Operator: yt_dlp.YoutubeDL = self.__ReinitializeOperator()

	def select_quality(self, quality: Qualities | int):
		"""
		Задаёт предпочитаемое качество видео.

		:param quality: Качество видео или высота кадра в пикселях.
		:type quality: Resolutions | int
		"""

		if type(quality) == int: self.__Quality = quality
		else: self.__Quality = cast(Qualities, quality).value

	def set_output_directory(self, directory: PathLike):
		"""
		Задаёт директорию для сохранения видео.

		:param directory: Путь к директории.
		:type directory: PathLike
		"""

		self.__OutputDirectory = Path(directory)
		self.__OutputDirectory.mkdir(exist_ok = True)

	def set_proxy(self, proxy: Proxy | str):
		"""
		Задаёт прокси-сервер для выполнения запросов.

		:param proxy: Прокси сервер.
		:type proxy: Proxy | str
		"""
		
		if type(proxy) == str: self.__Proxy = Proxy().parse(proxy)
		else: self.__Proxy = cast(Proxy, proxy)

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ РАБОТЫ С ВИДЕО <<<<< #
	#==========================================================================================#

	def download_video(self, url: str):
		"""
		Скачивает видео.

		:param url: Ссылка на видео.
		:type url: str
		"""

		self.__ReinitializeOperator()

		url = Validator_URL.parse(url)
		self.__Operator.download(ToSequence(url))

	def get_metainfo(self, url: str) -> dict | None:
		"""
		Получает метаданные видео.

		:param url: Ссылка на видео.
		:type url: str
		:return: Словарь метаданных или `None` при ошибке.
		:rtype: dict | None
		"""

		self.__ReinitializeOperator()

		url = Validator_URL.parse(url)
		MetadataBuffer = self.__Operator.extract_info(url, download = False)
		SanitizedMetadata = self.__Operator.sanitize_info(MetadataBuffer)
		
		if SanitizedMetadata: return dict(SanitizedMetadata.items())

		return None
