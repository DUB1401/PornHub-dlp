from Source.Core.Downloader import VideoDownloader

from dublib.CLI.Terminalyzer import Command, ParsedCommandData, Terminalyzer
from dublib.CLI.TextStyler import Colors, Decorations, TextStyler
from dublib.Methods.Filesystem import ReadTextFile
from dublib.Methods.System import Clear
from dublib.CLI import readline

import shlex
import os

class LiveCLI:
	"""Live CLI режим работы приложения."""

	#==========================================================================================#
	# >>>>> СВОЙСТВА <<<<< #
	#==========================================================================================#

	@property
	def commands(self) -> list[Command]:
		"""Список команд Live режима."""

		CommandsList = list()

		Com = Command("clear", "Cleare console.")
		CommandsList.append(Com)

		Com = Command("exit", "Exit live mode.")
		CommandsList.append(Com)

		return CommandsList

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __ProcessCommand(self, command: ParsedCommandData):
		"""
		Проводит обработку комманды.
			command – комманда.
		"""

		if command.name == "exit": 
			exit(0)

		elif command.name == "clear":
			Clear()

	def __ProcessMacros(self, macros: str) -> bool:
		"""
		Проводит обработку макросов.
			macros – макрос.
		"""

		IsProcessed = False

		if self.__Downloader.check_link(macros):
			IsProcessed = True
			self.__Downloader.download_video(macros, self.__Settings["quality"])

		elif os.path.exists(macros):
			IsProcessed = True
			Links = ReadTextFile(macros, "\n")
			Links = filter(lambda Element: bool(Element), Links)
			for Link in Links: self.__Downloader.download_video(Link, self.__Settings["quality"])

		return IsProcessed

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self, settings: dict):
		"""
		Live CLI режим работы приложения.
			settings – глобальные настройки.
		"""

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Settings = settings.copy()

		self.__Analyzer = Terminalyzer()
		self.__Downloader = VideoDownloader()

		self.__Analyzer.helper.enable()
		
	def run(self):
		"""Запускает цикл ввода команд."""

		Clear()
		ExitBold = TextStyler("exit").decorate.bold
		print(TextStyler("PornHub-dlp v2.1.0").decorate.bold)
		print(f"Вы находитесь в Live-режиме консольного интерфейса. Для выхода выполните {ExitBold} или нажмите Ctrl + C.")
		print("Введите ссылку на видеоролик или путь к текстовому файлу, из которого нужно извлечь список ссылок.")
		print("Проект на GitHub:" + " ", end = "")
		TextStyler("https://github.com/DUB1401/PornHub-dlp", text_color = Colors.Cyan, decorations = Decorations.Italic).print()
		print()

		while True:
			Input = None

			try:
				Input = input("PornHub-dlp > ").strip()

			except KeyboardInterrupt:
				print("exit")
				exit(0)

			if Input:
				if self.__ProcessMacros(Input): continue
				self.__Analyzer.set_source(shlex.split(Input))
				ParsedCommand = self.__Analyzer.check_commands(self.commands)

				if ParsedCommand: self.__ProcessCommand(ParsedCommand)
				elif not Input.startswith("help"): print(TextStyler("[ERROR] Неизвестная команда.").colorize.red)