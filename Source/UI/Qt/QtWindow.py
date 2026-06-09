from Source.UI.Qt.yt_dlp import yt_dlp

from PyQt6.QtWidgets import (
	QCheckBox, 
	QComboBox,
	QGroupBox, 
	QLabel, 
	QMainWindow, 
	QProgressBar, 
	QPushButton, 
	QTextEdit,
	QVBoxLayout
)
from PyQt6.QtGui import QCursor, QDesktopServices, QMovie, QTextCursor
from PyQt6.QtCore import Qt,QSize, QThread, QUrl
from dublib.Engine.GetText import _

import pyperclip
import json
import time
import os
import re

class PlainTextEdit(QTextEdit):
	"""Поле ввода неформатированного текста."""

	def __init__(self, parent = None):
		super().__init__(parent)

	def insertFromMimeData(self, source):
		self.insertPlainText(source.text())

class QtWindow(QMainWindow):
	"""Главное окно (Qt)."""

	#==========================================================================================#
	# >>>>> ОБРАБОТЧИКИ СИГНАЛОВ <<<<< #
	#==========================================================================================#

	def __Clear(self):
		self.Input.clear()
		self.Output.clear()
		self.ProgressBar.setValue(0)
		self.__VideoLinks = list()

	def __CopyOutput(self):

		try: pyperclip.copy(self.Output.toPlainText())
		except pyperclip.PyperclipException: self.Print("On GNU/Linux you can install <b>xclip</b> or <b>xselect</b> to enable a copy/paste mechanism.")

	def __DownloadVideos(self):
		self.Output.clear()
		self.__RemoveRepeatedLinks()
		self.Clear.setEnabled(False)
		self.Download.setEnabled(False)
		self.Output.setReadOnly(True)
		self.Paste.setEnabled(False)
		self.__VideoLinks = list(filter(None, self.Input.toPlainText().strip().split('\n')))
		self.ProgressBar.setMaximum(len(self.__VideoLinks))
		self.ProgressBar.setValue(0)
		self.ProgressBar.setVisible(True)
		self.__StartDownloading()

	def __FormatInput(self):
		InputText = self.Input.toPlainText()
		InputLines = InputText.split('\n')
		FormattedLines = list() 
		ResultLines = list()
		ResultText = None

		for Line in InputLines:
			Bufer = Line.replace("https", "\nhttps").strip("\n \t")
			FormattedLines += Bufer.split('\n')
		
		for Line in FormattedLines:
			Line = Line.split('&')[0]
			if bool(re.match(r"https:\/\/(?:\w{0,4}\.)?pornhub\.(org|com)\/view_video\.php\?viewkey=\w+", Line)): ResultLines.append(Line)

		ResultText = "\n".join(ResultLines) + "\n"

		if ResultText.strip("\n \t") == "":
			ResultText = ""
			self.Download.setEnabled(False)

		elif self.__VideoIndex == 0:
			self.Download.setEnabled(True)

		if ResultText != self.Input.toPlainText():
			self.Input.setText(ResultText)

		self.Input.moveCursor(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.MoveAnchor)

	def __OpenGitHub(self):
		QDesktopServices.openUrl(QUrl("https://github.com/DUB1401/PornHub-dlp"))

	def __Paste(self):
		try: self.Input.setText(self.Input.toPlainText() + pyperclip.paste().strip("\n \t") + "\n") 
		except pyperclip.PyperclipException: self.Print("On GNU/Linux you can install <b>xclip</b> or <b>xselect</b> to enable a copy/paste mechanism.")

	def __SaveSetting(self, Key: str, Value):
		self.__Settings[Key] = Value
		Bufer = self.__Settings.copy()

		if Bufer["directory"] == os.getcwd() + "/Downloads":
			Bufer["directory"] = ""

		with open("Settings.json", "w", encoding = "utf-8") as FileWrite:
			json.dump(Bufer, FileWrite, ensure_ascii = False, indent = '\t', separators = (",", ": "))

	def __ScrollOutputToEnd(self):
		self.Output.moveCursor(QTextCursor.MoveOperation.End)

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __CreateBasicUI(self):

		# self.AdsBox = QGroupBox(self)
		# self.AdsBox.move(870, 170)
		# self.AdsBox.resize(200, 300)
		# self.AdsBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
		# self.AdsBox.setTitle(f"📰 " + _("Реклама"))

		self.Clear = QPushButton(self)
		self.Clear.clicked.connect(self.__Clear)
		self.Clear.move(870, 590)
		self.Clear.resize(200, 40)
		self.Clear.setText(f"🧹 " + _("Очистить"))

		self.Copy = QPushButton(self)
		self.Copy.clicked.connect(self.__CopyOutput)
		self.Copy.move(870, 540)
		self.Copy.resize(200, 40)
		self.Copy.setText(f"📋 " + _("Копировать вывод"))
		self.Copyright = QLabel(self)
		self.Copyright.setText("Copyright © 2023-2026. DUB1401.")
		self.Copyright.move(10, 690)
		self.Copyright.adjustSize()

		self.Download = QPushButton(self)
		self.Download.clicked.connect(self.__DownloadVideos)
		self.Download.move(870, 640)
		self.Download.resize(200, 40)
		self.Download.setEnabled(False)
		self.Download.setText(f"⬇ " + _("Скачать"))

		self.Input = PlainTextEdit(self)
		self.Input.move(10, 10)
		self.Input.resize(850, 420)
		self.Input.setPlaceholderText(_("Вставьте сюда ссылки на видео"))
		self.Input.textChanged.connect(self.__FormatInput)

		self.Link = QLabel(self)
		self.Link.linkActivated.connect(self.__OpenGitHub)
		self.Link.setText("<a href=\"https://github.com/DUB1401/PornHub-dlp\">GitHub</a>")
		self.Link.adjustSize()
		self.Link.move(1080 - self.Link.size().width() - 10, 690)

		self.Output = QTextEdit(self)
		self.Output.move(10, 490)
		self.Output.resize(850, 190)
		self.Output.setReadOnly(True)
		self.Output.setPlaceholderText(_("Вывод"))
		self.Output.textChanged.connect(self.__ScrollOutputToEnd)

		self.Paste = QPushButton(self)
		self.Paste.clicked.connect(self.__Paste)
		self.Paste.move(870, 490)
		self.Paste.resize(200, 40)
		self.Paste.setText(f"📖 " + _("Вставить ссылки"))

		self.ProgressBar = QProgressBar(self)
		self.ProgressBar.move(10, 450)
		self.ProgressBar.resize(850, 20)
		self.ProgressBar.setValue(0)

		self.SettingsBox = QGroupBox(self)
		self.SettingsBox.move(870, 10)
		self.SettingsBox.resize(200, 160)
		self.SettingsBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.SettingsBox.setTitle(f"🔧 " + _("Настройки"))

	def __CreateSettingsGroupUI(self):
		SettingsLayout = QVBoxLayout()
		self.SettingsBox.setLayout(SettingsLayout)

		#---> Создание объектов GUI.
		#==========================================================================================#

		CualityTitle = QLabel(self)
		CualityTitle.setText(_("Качество") + ":")
		CualityTitle.adjustSize()

		CualitySelecter = QComboBox(self)
		CualitySelecter.addItems(("4K", "2K", "FullHD", "HD", "480p", "360p", "240p"))
		CualitySelecter.setCurrentIndex(self.__Settings["quality"])
		CualitySelecter.currentIndexChanged.connect(lambda: self.__SaveSetting("quality", CualitySelecter.currentIndex()))
		CualitySelecter.resize(180, 40)
		CualitySelecter.setToolTip(_("Разрешение скачиваемых видео."))

		SortByModel = QCheckBox(self)
		SortByModel.clicked.connect(lambda: self.__SaveSetting("sorting", SortByModel.isChecked()))
		SortByModel.setChecked(self.__Settings["sorting"])
		SortByModel.setText(_("По моделям"))
		SortByModel.setToolTip(_("Сортировать видео по каталогам в соответствии с авторами."))
		SortByModel.adjustSize()

		ComToOrg = QCheckBox(self)
		ComToOrg.clicked.connect(lambda: self.__SaveSetting("com_to_org", ComToOrg.isChecked()))
		ComToOrg.setChecked(self.__Settings["com_to_org"])
		ComToOrg.setText(_("Использовать *.org"))
		ComToOrg.setToolTip(_("Подменяет в ссылках домен первого уровня *.com на *.org."))
		ComToOrg.adjustSize()
		
		#---> Добавление объектов GUI в слой.
		#==========================================================================================#
		SettingsLayout.addWidget(SortByModel)
		SettingsLayout.addWidget(ComToOrg)
		SettingsLayout.addWidget(CualityTitle)
		SettingsLayout.addWidget(CualitySelecter)
		SettingsLayout.addStretch()

	def __EndDownloading(self, ExitCode: int):
		self.__VideoIndex += 1
		self.ProgressBar.setValue(self.__VideoIndex)

		if ExitCode == 0:
			self.Print("<b style=\"color: green;\">Done!</b> (" + self.__FormatExecutionTime(round(float(time.time() - self.__StartTime), 2)) + ")", True)

		else:
			self.Print("<b style=\"color: red;\">Error!</b> See console output for more information.", True)

		self.Input.setText('\n'.join(self.Input.toPlainText().split('\n')[1:]))

		if self.__VideoIndex < len(self.__VideoLinks):
			self.__StartDownloading()

		else:
			self.Print("Complete.")
			self.Clear.setEnabled(True)
			self.Download.setEnabled(True)
			self.Output.setReadOnly(False)
			self.Paste.setEnabled(True)
			self.__VideoIndex = 0
			self.Input.setText("")

	def __FormatExecutionTime(self, ExecutionTime: float) -> str:
		Result = ""
		ElapsedMinutes = int(ExecutionTime / 60.0)

		if ElapsedMinutes > 0:
			Result += str(ElapsedMinutes) + " minutes "
			ElapsedSeconds = round(ExecutionTime % 60.0, 2)
			Result += str(ElapsedSeconds) + " seconds"

		else:
			Result += str(ExecutionTime) + " seconds"

		return Result

	def __RemoveRepeatedLinks(self):
		InputText = self.Input.toPlainText()
		InputLines = InputText.split('\n')
		ResultLines = [*set(InputLines)]

		if len(InputLines) != len(ResultLines):
			ResultText = "\n".join(ResultLines) + "\n"
			self.Input.setText(ResultText)
			RepeatedLinksCount = len(InputLines) - len(ResultLines)
			self.Print("<b>Removed identical links count:</b> " + str(RepeatedLinksCount), True)

	def __StartDownloading(self):
		SaveDirectory = self.__Settings["directory"]

		self.__StartTime = time.time()

		if self.__VideoIndex < len(self.__VideoLinks):
			CurrentLink = self.__VideoLinks[self.__VideoIndex]
			if self.__Settings["com_to_org"]: CurrentLink = CurrentLink.replace("pornhub.com", "pornhub.org")
			self.Print("<b>Downloading: </b>" + str(self.__VideoIndex + 1) + " / " + str(len(self.__VideoLinks)))
			self.Print("<b>Current task:</b> <i>" + self.__VideoLinks[self.__VideoIndex] + "</i>")
			self.Subprocess = yt_dlp(SaveDirectory, CurrentLink, self.__Settings["sorting"], self.__Resolutions[self.__Settings["quality"]])
			self.Subprocess.moveToThread(self.__DownloadingThread)
			self.__DownloadingThread.quit()
			self.__DownloadingThread.started.connect(self.Subprocess.run)
			self.Subprocess.finished.connect(self.__EndDownloading)
			self.Subprocess.finished.connect(self.__DownloadingThread.quit)
			self.__DownloadingThread.start()

	def __init__(self, settings: dict):
		"""
		Главное окно (Qt).
			settings – словарь глобальных настроек.
		"""

		super().__init__()

		self.__Resolutions = ("4096", "2048", "1080", "720", "480", "360", "240")
		self.__DownloadingThread = None
		self.__VideoLinks = list()
		self.__StartTime = None
		self.__VideoIndex = 0

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__Settings = settings.copy()

		self.__DownloadingThread = QThread()

		#---> Инициализация графического интерфейса.
		#==========================================================================================#

		self.setFixedSize(1080, 720)
		self.setWindowTitle("PornHub-dlp v2.1.0")

		self.__CreateBasicUI()
		self.__CreateSettingsGroupUI()

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def Print(self, Message: str, Separator: bool = False):

		Text = ""
		if not self.Output.toPlainText(): Text = ""
		else: Text = self.Output.toHtml()
		if Separator: Message += "<br>=========================================================================================="
		self.Output.setHtml(Text + Message)