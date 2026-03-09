
#creating a new virtual environment
- python -m venv <virtual env name>

#activating the virtual env
- source <name>/bin/activate #linux
- source <name>/Scripts/activate #windows

#installing pip libraries
- pip install pdfplumber
- pip install pyinstaller

#creating the exec file, this will create some directories and the 
#the executable will be located in the "dist" directory
# *very important: must run this in the root directory and especify the path to script, ej: scripts/frame.py
- pyinstaller --onefile -w --name <wished name>.exe scripts/frame.py
# if the previous line doesn't work, run this:
- pyinstaller --onefile -w --name <wished name> --collect-submodules numpy --collect-submodules pandas scripts/frame.py