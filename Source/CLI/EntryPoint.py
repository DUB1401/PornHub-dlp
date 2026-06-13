from Source.Core.BaseProcessor import BaseProcessor

from dublib.CLI.Terminalyzer import Command, ParsedCommandData, Terminalyzer
from dublib.CLI.TextStyler import Codes, GetStyledTextFromHTML, TextStyler
from dublib.CLI.Validators import Validator_URL, Validator_ValidPath
from dublib.Exceptions.CLI.Validators import ValidationError
from dublib.Methods.Filesystem import ReadTextFile
from dublib.CLI.Templates.Bus import PrintError
from dublib.Methods.System import Clear
from dublib.WebRequestor import Proxy
from dublib.CLI import readline

from pathlib import Path
import shlex
import os

from yt_dlp.version import __version__
import pyfiglet

class Interface:
	"""Обработчик CLI."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def selector(self) -> str:
		"""Указатель ввода."""

		BOLD_GREEN = TextStyler(decorations = Codes.Decorations.Bold, text_color = Codes.Colors.Green)

		return BOLD_GREEN.get_styled_text("spicydl ->") + " "

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __ExecuteBaseCoomands(self, command: ParsedCommandData):
		"""
		Обрабатывает базовые команды.

		:param command: Команда.
		:type command: ParsedCommandData
		"""

		match command.name:
			case "clear": Clear()
			case "exit": exit(0)

	def __GenerateBaseCommands(self) -> list[Command]:
		"""
		Генерирует последовательность описаний базовых команд.

		:return: Последовательность описаний базовых команд.
		:rtype: list[Command]
		"""

		Commands: list[Command] = list()

		Com = Command("clear", "Clear terminal.")
		Commands.append(Com)

		Com = Command("exit", "Exit from application.")
		Commands.append(Com)

		return Commands

	def __ExtractLinks(self, file: Path) -> tuple[str, ...]:
		"""
		Извлекает ссылки из файла.

		:param file: Путь к текстовому файлу со ссылками.
		:type file: Path
		:return: Последовательность ссылок.
		:rtype: tuple[str, ...]
		"""

		UnprocessdeLines: tuple[str, ...] = ReadTextFile(file, split = True)
		Links: list[str] = list()

		for Line in UnprocessdeLines:
			Line = Line.strip()
			if " #" in Line: Line = Line.split(" #", maxsplit = 1)[0].rstrip()
			if Validator_URL.validate(Line): Links.append(Line)
			
		return tuple(Links)

	def __ProcessLink(self, input_line: str) -> bool:
		"""
		Обрабатывает передачу URL.

		:param input_line: Введённая строка.
		:type input_line: str
		:return: Возвращает `True`, если была введена ссылка.
		:rtype: bool
		"""

		IsURL: bool = Validator_URL.validate(input_line)
		if IsURL: self.__Processor.download_video(input_line)

		return IsURL

	def __ProcessTextFile(self, input_line: str) -> bool:
		"""
		Обрабатывает передачу пути к текстовому файлу.

		:param input_line: Введённая строка.
		:type input_line: str
		:return: Возвращает `True`, если был передан путь к существующему файлу.
		:rtype: bool
		"""

		IsValidPath: bool = False

		try: 
			TextFilePath: Path = Validator_ValidPath.parse(input_line)
			IsValidPath = True
		except ValidationError: return IsValidPath

		Links = self.__ExtractLinks(TextFilePath)

		print("Links extracted:", len(Links))

		for Link in Links: self.__Processor.download_video(Link)

		return IsValidPath

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ ШАБЛОНЫ ВЫВОДА <<<<< #
	#==========================================================================================#

	def __PrintDebugInfo(self):
		"""Выводит отлаточную информацию."""

		print(GetStyledTextFromHTML(f"<b>yt-dlp</b> version: <i>{__version__}</i>"))

		ProxyString: str | None = os.getenv("HTTPS_PROXY")
		if ProxyString:
			ProxyObject = Proxy().parse(ProxyString)
			print(GetStyledTextFromHTML(f"Loaded proxy: <i>{ProxyObject.host}</i>"))

	def __PrintGreeting(self):
		"""Выводит стартовое сообщение."""

		print(pyfiglet.figlet_format("SpicyDL"))
		print("For starting downloading put video URL or path to text file with URLs separated by newlines.")
		print(GetStyledTextFromHTML("<i>Need help? Print <b>help</b>!</i>"))

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):
		"""Обработчик CLI."""

		self.__BaseCommands: list[Command] = self.__GenerateBaseCommands()
		self.__Analyzer = Terminalyzer()
		self.__Analyzer.helper.enable()
		self.__Processor: BaseProcessor = BaseProcessor()

	def run(self):
		"""Запускает обработчик CLI."""

		self.__PrintGreeting()
		self.__PrintDebugInfo()
		
		while True:
			InputLine: str = input(self.selector).strip()

			if self.__ProcessLink(InputLine): continue
			if self.__ProcessTextFile(InputLine): continue

			InputParameters = shlex.split(InputLine) if len(InputLine) > 0 else None
			
			if InputLine:
				self.__Analyzer.set_input(InputParameters)
				CommadData = self.__Analyzer.check_commands(self.__BaseCommands)
				if CommadData: self.__ExecuteBaseCoomands(CommadData)
				else: PrintError("Unknown command or invalid input data.")
			