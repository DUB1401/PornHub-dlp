:: Переход в директорию проекта.
cd ..\..\

:: Сборка приложения.
pyinstaller --distpath %~dp0\Release --i icon.ico --version-file Build\Windows\metadata.txt --onefile main.py --name pornhub-dlp

:: Копирование в директорию сборки необходимых компонентов приложения.
xcopy /Y /I /S Locales Build\Windows\Release\Locales
xcopy /Y icon.ico Build\Windows\Release
xcopy /Y Settings.json Build\Windows\Release

:: Удаление файлов сборки приложения.
rmdir /q /s Build\pornhub-dlp
del pornhub-dlp.spec
