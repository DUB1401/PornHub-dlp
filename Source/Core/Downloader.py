from dublib.Engine.Bus import ExecutionError, ExecutionStatus
from dublib.Methods.Filesystem import NormalizePath

import urllib.request
import subprocess
import zipfile
import json
import sys
import os

import re

class VideoDownloader:
	"""Загрузчик видео."""

	#==========================================================================================#
	# >>>>> ПРИВАТНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __CheckLibs(self):
		"""Проверяет, загружены ли нужные библиотеки."""

		if not os.path.exists(f"yt-dlp/{self.__LibName}"):
			if not os.path.exists("yt-dlp"): os.makedirs("yt-dlp")
			print("Downloading yt-dlp... ", end = "", flush = True)
			urllib.request.urlretrieve(f"https://github.com/yt-dlp/yt-dlp/releases/download/2025.01.12/{self.__LibName}", f"yt-dlp/{self.__LibName}")
			print("Done.")

			if sys.platform == "linux":
				print("Making yt-dlp executable... ", end = "")
				os.system("chmod u+x yt-dlp/yt-dlp")
				print("Done.")

		if sys.platform == "win32" and not os.path.exists("yt-dlp/ffmpeg.exe"):
			print("Downloading ffmpeg 7.1 Essentials (Windows build)... ", end = "", flush = True)
			urllib.request.urlretrieve("https://github.com/GyanD/codexffmpeg/releases/download/7.1/ffmpeg-7.1-essentials_build.zip", "yt-dlp/ffmpeg-essentials.zip")
			print("Done.")

			with zipfile.ZipFile("yt-dlp/ffmpeg-essentials.zip", "r") as ZipReader:
				print("Exracting files...", flush = True)
				with open("yt-dlp/ffmpeg.exe", "wb") as FileWriter: FileWriter.write(ZipReader.read("ffmpeg-7.1-essentials_build/bin/ffmpeg.exe"))
				print("ffmpeg.exe")
				with open("yt-dlp/ffprobe.exe", "wb") as FileWriter: FileWriter.write(ZipReader.read("ffmpeg-7.1-essentials_build/bin/ffprobe.exe"))
				print("ffprobe.exe")
				print("Done.")

				try:
					os.remove("yt-dlp/ffmpeg-essentials.zip")
					print("Temporary files removed.")

				except: pass

	#==========================================================================================#
	# >>>>> ПУБЛИЧНЫЕ МЕТОДЫ <<<<< #
	#==========================================================================================#

	def __init__(self):

		#---> Генерация динамических атрибутов.
		#==========================================================================================#
		self.__IsSortingEnabled = None
		self.__DownloadsDirectory = "Downloads"
		self.__LibName = "yt-dlp.exe" if sys.platform == "win32" else "yt-dlp"

		self.__CheckLibs()

	def check_link(self, link: str) -> bool:
		"""
		Проверяет, подходит ли ссылка по формату.
			link – ссылка на видео.
		"""

		return bool(re.match(r"https:\/\/.{0,4}?pornhub\.com\/view_video\.php\?viewkey=\S+\b", link))

	def download_video(self, link: str, quality: int | str) -> ExecutionStatus:
		"""
		Возвращает словарь данных видео.
			link – ссылка на видео;\n
			quality – предпочитаемое качество видео.
		"""

		Status = ExecutionStatus(0)
		quality = self.get_video_height(quality)
		VideoInfoStatus = self.get_video_info(link)

		if VideoInfoStatus.code != 0: return VideoInfoStatus
		if self.__DownloadsDirectory == "Downloads" and not os.path.exists(self.__DownloadsDirectory): os.makedirs(self.__DownloadsDirectory)

		FfmpegPath = ""

		if sys.platform == "win32": FfmpegPath = "--ffmpeg-location yt-dlp/ffmpeg.exe"

		try:
			Data = VideoInfoStatus.value
			Filename = Data["filename"]
			Uploader = ""
			if self.__IsSortingEnabled: Uploader = "/" + Data["uploader"]
			Path = NormalizePath(f"yt-dlp/{self.__LibName}")
			ExitCode = os.system(f"{Path} -f \"bv*[height<={quality}]+ba/b[height<={quality}]\" -o \"{self.__DownloadsDirectory}{Uploader}/{Filename}\" {link} {FfmpegPath}")
			if ExitCode != 0: Status = ExecutionError(ExitCode, "Unable to download video.")

		except Exception as ExceptionData:
			Status = ExecutionError(-1, str(ExceptionData))

		return Status

	def enable_sorting(self, status: bool):
		"""
		Переключает сортировку по каталогам в соответствии с автором видео.
			status – статус использования.
		"""

		self.__IsSortingEnabled = status

	def get_video_height(self, quality: int | str) -> int | None:
		"""
		Возвращает высоту кадра видео.
			quality – предпочитаемое качество видео.
		"""

		quality = str(quality)

		QualityTypes = {
			"4k": 4096,
			"2k": 2048,
			"fullhd": 1080,
			"hd": 720,
			"480p": 480,
			"360p": 360,
			"240p": 240
		}
		Quality = None
		
		if quality.isdigit() and len(quality) == 1:
			Index = int(quality)
			Quality = tuple(QualityTypes.values())[Index]

		elif quality.isdigit():
			Quality = int(quality)

		elif quality.lower() in QualityTypes.keys():
			Quality = QualityTypes[quality.lower()]

		return Quality

	def get_video_info(self, link: str) -> ExecutionStatus:
		"""
		Возвращает словарь данных видео.
			link – ссылка на видео.
		"""

		Status = ExecutionStatus(0)

		try:
			Path = NormalizePath(f"yt-dlp/{self.__LibName}")
			Output = subprocess.getoutput(f"{Path} --dump-json {link}")
			Status.value = json.loads(Output)

		except Exception as ExceptionData:
			print(Output)
			Status = ExecutionError(-1, str(ExceptionData), Output)

		return Status
	
	def set_downloads_directory(self, path: str):
		"""
		Задаёт путь к каталогу для скачивания видео.
			path – путь.
		"""

		if not os.path.exists(): raise FileNotFoundError(path)
		self.__DownloadsDirectory = NormalizePath(path)