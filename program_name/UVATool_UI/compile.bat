@echo off 

call ./build_ui_file.bat

echo THIS SCRIPT WILL BUILD THE DIST FILE

set BUILD_DIRECTORY=build
set FILE_NAME=form_uvatool
set UI_FILE=%FILE_NAME%.ui
SET OUTPUT_FILE=%BUILD_DIRECTORY%\%FILE_NAME%.py

@REM pyinstaller -onefile %OUTPUT_FILE% -windowed --icon=.\icons\UVATool_main_window.png
pyinstaller --onefile --icon=.\icons\UVATool_main_window.png %OUTPUT_FILE% --windowed

copy .\icons\* .\dist\icons

echo SCRIPT ENDING...