@echo off 

call ./build_ui_file.bat

echo THIS SCRIPT WILL BUILD THE DIST FILE

set BUILD_DIRECTORY=build
set FILE_NAME=form_uvatool
set UI_FILE=%FILE_NAME%.ui
SET OUTPUT_FILE=%BUILD_DIRECTORY%\%FILE_NAME%.py
set ICONS=.\dist\%FILE_NAME%\icons\

echo EXECUTING: pyinstaller --onefile --icon=.\icons\UVATool_main_window.png %OUTPUT_FILE% --windowed

@REM --onefile make the program binary slow - preffer the normal output
@REM TO USE THIS COMMAND, UNCOMENT ALL LINES
@REM set ICONS=.\dist\icons\
@REM pyinstaller --onefile --icon=.\icons\UVATool_main_window.png %OUTPUT_FILE% --windowed

echo EXECUTING: pyinstaller --icon=.\icons\UVATool_main_window.png %OUTPUT_FILE% --windowed

pyinstaller --icon=.\icons\UVATool_main_window.png %OUTPUT_FILE% --windowed

ECHO EXECUTING: set ICONS=.\dist\icons\

ECHO EXECUTING: mkdir %ICONS%
mkdir %ICONS%

echo EXECUTING: copy .\icons\* %ICONS%
copy .\icons\* %ICONS%

echo SCRIPT ENDING...