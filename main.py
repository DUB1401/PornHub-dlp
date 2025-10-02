from Source.Core.Application import Application, Interfaces

from dublib.Methods.System import CheckPythonMinimalVersion
from dublib.CLI.Terminalyzer import Command, Terminalyzer
from dublib.Methods.Filesystem import ReadJSON
from dublib.Engine.GetText import GetText

import warnings
import locale

from dotenv import load_dotenv

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ <<<<< #
#==========================================================================================#

CheckPythonMinimalVersion(3, 10)
load_dotenv()
warnings.filterwarnings("ignore", category = DeprecationWarning)
GetText.initialize("PornHub-dlp", locale.getdefaultlocale()[0], "Locales")
Settings = ReadJSON("Settings.json")
WindowObject = Application(Settings)

#==========================================================================================#
# >>>>> ГЕНЕРАЦИЯ ОПИСАНИЙ КОМАНД <<<<< #
#==========================================================================================#

CommandsList = list()
Com = Command("run", "Run application.")
ComPos = Com.create_position("MODE", "Mode of launching.")
ComPos.add_flag("qt", "PyQt6 mode.")
ComPos.add_flag("gtk", "GTK4 mode.")
ComPos.add_flag("live", "Live CLI mode.")
CommandsList.append(Com)

Analyzer = Terminalyzer()
Analyzer.enable_help()
ParsedCommand = Analyzer.check_commands(CommandsList)

#==========================================================================================#
# >>>>> ОБРАБОТКА КОМАНД <<<<< #
#==========================================================================================#

if not ParsedCommand: WindowObject.run(Interfaces.Qt)
elif ParsedCommand.check_flag("live"): WindowObject.run(Interfaces.LiveCLI)
elif ParsedCommand.check_flag("qt"): WindowObject.run(Interfaces.Qt)