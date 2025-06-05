pyinstaller app\sysTray.py ^
--onefile ^
--icon=translate_icon.ico ^
--noconsole ^
--add-data "translate_icon.ico;." ^
--add-data "phrase_dict.json;." ^
--name MisType

rmdir build /S /Q
del MisType.spec
move dist\MisType.exe .
rmdir dist
cls