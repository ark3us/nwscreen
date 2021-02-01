# NWN Screenshot Composer
Applicazione per creare collage di dialoghi.

## Creazione dell'eseguibile
### Windows
```
type nul > matplotlibrc
pyinstaller.exe --onefile --add-data "matplotlibrc;." .\nwscreen.py
```
### Linux
```
touch matplotlibrc
pyinstaller --onefile --add-data "matplotlibrc:." ./nwscreen.py
```