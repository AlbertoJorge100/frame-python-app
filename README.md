
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
- pyinstaller --onefile -w --name <wished name>.exe <script>.py
