:: This file is used to create the documentation for the project. using the pdoc python package.
:: This file is not required for the project to run.
:: it runs the setup.bat file to install the reinstall the packages.
call setup.bat
pip install pdoc
rmdir /s /q docs
pdoc ./Application/main.py ./Application/functions.py ./standard_widgets.py ZMK ListUnion pykle_serial -o ./docs