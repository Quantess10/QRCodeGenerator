from cx_Freeze import setup, Executable
import sys

# Dodajemy ścieżki do obrazów lub folderów z obrazami
include_files = [
    'ikona.ico',
    'main_image.jpg',
]
build_options = {
    'packages': [],
    'excludes': [],
    'include_files': include_files
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
