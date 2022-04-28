@echo off 
@REM HOW TO EXECUTE : JUST OPEN THIS FILE IN TERMINAL USING ./build.bat (windows users)

set BUILD_DIRECTORY=build
set ICONS_DIRECTORY=icons
set BUILD_FILE=form_uvatool
@REM set BUILD_FILE=form_results
@REM set BUILD_FILE=form_draw
set UI_FILE=%BUILD_FILE%.ui
SET OUTPUT_FILE=%BUILD_DIRECTORY%\%BUILD_FILE%.py

@REM CREATING BUILD FOLDER OUTPUT
if exist %BUILD_DIRECTORY% (
  echo BUILD FOLDER ALREADY EXIST
) else (
  mkdir %BUILD_DIRECTORY%
)

@REM CREATING BUILD FOLDER OUTPUT
if exist %ICONS_DIRECTORY% (
  echo ICONS FOLDER ALREADY EXIST
) else (
  mkdir %ICONS_DIRECTORY%
)

@REM PROCESSING UI FILES
echo EXECUTING: pyuic5 -x %UI_FILE% -o %OUTPUT_FILE%
pyuic5 -x %UI_FILE% -o %OUTPUT_FILE%

@REM copy .\uvat.py .\build\
copy .\icons\*.png .\build\icons

echo SCRIPT ENDING...