@REM HOW TO EXECUTE : JUST OPEN THIS FILE IN TERMINAL USING ./exec.bat (windows users)

@REM BUILD FOLDER OUTPUT
mkdir build

@REM BUILDING
pyuic5 -x ./uvatool.ui -o ./build/uvatool.py

@REM EXECUTING
python ./build/uvatool.py