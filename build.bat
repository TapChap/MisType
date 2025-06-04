pyinstaller app\sysTray.py ^
--onefile ^
--icon=translate_icon.ico ^
--add-data "translate_icon.ico;." ^
--noconsole ^
--name MisType

rmdir build /S /Q
del MisType.spec
move dist\MisType.exe .
rmdir dist
cls