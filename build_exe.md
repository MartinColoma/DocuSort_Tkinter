# Building Tkinter as .EXE Application (Windows Version)
*Note: If you have virtual environment, make sure you are inside your virtual env.*

1. Run the following to enter your virtual env (Windows Version):
```bash
Set-ExecutionPolicy Unrestricted -Scope Process
```
```bash
.venv\Scripts\activate
```

2. Install PyInstaller package through terminal
```bash
pip install PyInstaller
```

3. Use PowerShell Terminal then run this code:

```bash
pyinstaller --onefile --windowed --add-data "resources\*;resources" --add-data "docusortDB.db;." DocuSort.py
```
Change the directory basing on your project/folder structure.

4. After building EXE run this code to run the newly built application:
```bash
dist/DocuSort.exe
```