# PornHub Downloader
**PornHub Downloader** – это приложение с графическим интерфейсом для массовой загрузки видео с [PornHub](https://www.pornhub.com/), поддерживающее сортировку по моделям и выбор предпочитаемого качества роликов.

## Порядок установки и использования | Исполняемый файл Windows
1. Загрузить последний релиз исполняемой версии. Распаковать.
2. Запустить _PornHub Downloader.exe_. Вставить в поле ввода список ссылок на видео и нажать кнопку загрузки.
3. Дождаться скачивания видео в  папку _Downloads_, в директории скрипта.

## Порядок установки и использования | Скрипт Python
1. Загрузить последний релиз скрипта. Распаковать.
2. Установить Python версии не старше 3.10. Рекомендуется добавить в PATH.
3. В среду исполнения установить следующие пакеты: [pyinstaller](https://github.com/pyinstaller/pyinstaller), [requests](https://github.com/psf/requests), [pyqt6](https://www.riverbankcomputing.com/software/pyqt/).
```
pip install pyinstaller
pip install requests
pip install pyqt6
```
Либо установить сразу все пакеты при помощи следующей команды, выполненной из директории скрипта.
```
pip install -r requirements.txt
```
4. Запустить _PornHub Downloader.py_. Вставить в поле ввода список ссылок на видео и нажать кнопку загрузки.
5. Дождаться скачивания видео в папку _Downloads_, в директории скрипта.

# Скриншот
![2023-08-11_12-41-08](https://github.com/DUB1401/PornHub-Downloader/assets/40277356/c319a663-3969-4a2f-8b7b-94a3438b4e0c)

# Сборка
1. Подготовить скрипт Python к работе согласно инструкции из порядка установки и использования.
2. Перейти в папку _Build_, внутри директории скрипта.
3. Запустить файл _build.bat_ и дождаться завершения работы.
4. Исполняемая версия будет помещена по адресу _Build/Release_ вместе со всеми зависимостями.

## Локализация
Для добавления сторонней локализации необходимо отредактировать файл [Locale.py](Source/Locale.py): в `LOCALES` указываются списки используемых программой строк на целевом языке, ключём должен являться двухбуквенный тег языка в верхнем регистре по стандарту **ISO 639-1**.

Доступные локализации: `EN`, `DE`, `PL`, `RU`, `UK`.

## Версии поставляемых бинарных файлов
| Файл    | Версия                        | Источник                                                           |
|---------|-------------------------------|--------------------------------------------------------------------|
| yt-dlp  | _2023.07.06_                  | [ссылка](https://github.com/yt-dlp/yt-dlp/releases/tag/2023.07.06) |
| ffmpeg  | _6.0 2023-03-04 (essentials)_ | [ссылка](https://github.com/GyanD/codexffmpeg/releases/tag/6.0)    |
| ffprobe | _6.0 2023-03-04 (essentials)_ | [ссылка](https://github.com/GyanD/codexffmpeg/releases/tag/6.0)    |

# Благодарность
* [@yt-dlp](https://github.com/yt-dlp) – библиотека загрузки потокового видео.

_Copyright © DUB1401. 2023._