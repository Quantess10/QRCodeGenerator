from cx_Freeze import setup, Executable
import sys

sys.setrecursionlimit(5000)
# Dodajemy ścieżki do obrazów lub folderów z obrazami
include_files = [
    'ikona.ico',
    'main_image.jpg',
]
build_options = {
    'packages': ['os', 'sys', 'tkinter', 'ttkthemes', 'qrcode', 'barcode', 'barcode.writer', 'PIL', 'io'],
    'excludes': [],
    'include_files': include_files,
    'optimize': 2
    }

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable(
        'qrgenerator.py',
        base=base,
        target_name='GeneratorKodow.exe',
        icon='ikona.ico'  # Tutaj ustawiasz ścieżkę do pliku ikony
    )
]

setup(name='Generator kodów',
    version='1.0',
    description='Generator kodów kreskowych i QR',
    options={'build_exe': build_options},
    executables=executables)
