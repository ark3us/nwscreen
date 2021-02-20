# NWN Screenshot Composer
Applicazione per creare collage di dialoghi.

## Creazione dell'eseguibile
### Windows
```
type nul > matplotlibrc
pyinstaller.exe --clean --onefile --add-data "matplotlibrc;." .\nwscreen.py
```
### Linux
```
touch matplotlibrc
pyinstaller --claen --onefile --add-data "matplotlibrc:." ./nwscreen.py
```