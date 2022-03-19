from sys import platform
from cx_Freeze import setup, Executable


base = None
if platform == 'win32':
    base = 'Win32Gui'

setup(
    name='screenshot_para_texto',
    version='1.0',
    description='Ferramenta de captura que transforma texto da imagem em string',
    options={
        'build_exe': {
            'includes': ['tkinter', 'ttkthemes', 'pyautogui', 'cv2', 'pytesseract', 'numpy']
        }
    },
    executables = [
        Executable(script='screenshot_para_texto.py', base=base, icon='screenshot.ico')
    ]
)