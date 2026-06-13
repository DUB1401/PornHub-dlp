from Source.CLI.EntryPoint import Interface

from dotenv import load_dotenv

load_dotenv()
InterfaceProcessor = Interface()
InterfaceProcessor.run()