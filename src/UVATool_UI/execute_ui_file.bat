@echo off 
@REM HOW TO EXECUTE : JUST OPEN THIS FILE IN TERMINAL USING ./execute.bat (windows users)

@REM call ./build_ui_file.bat

set BUILD_DIRECTORY=build
set FILE_NAME=form_uvatool
set UI_FILE=%FILE_NAME%.ui
SET OUTPUT_FILE=%BUILD_DIRECTORY%\%FILE_NAME%.py

@REM EXECUTING
echo EXECUTING: python %OUTPUT_FILE%
python %OUTPUT_FILE%