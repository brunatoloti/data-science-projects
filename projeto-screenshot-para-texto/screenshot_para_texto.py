import cv2
import pyautogui
import numpy as np
import pytesseract
from tkinter import Tk, ttk, Button, Text
from ttkthemes import ThemedTk


janela = ThemedTk(theme='radiance')
janela.title('Captura de texto em imagens')
janela.iconbitmap('screenshot.ico')



def screenshot_cut():
    im = pyautogui.screenshot()
    im = cv2.cvtColor(np.array(im),
                        cv2.COLOR_RGB2BGR)
    roi = cv2.selectROI(im)
    im_cropped = im[int(roi[1]):int(roi[1]+roi[3]),
                    int(roi[0]):int(roi[0]+roi[2])]
    cv2.imshow('cropped', im_cropped)
    cv2.destroyAllWindows()
    
    pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\Tesseract.exe"
    config_pytesseract = r'--oem 3 --psm 6'
    resultado = pytesseract.image_to_string(im_cropped, config=config_pytesseract, lang='por')
    texto_da_imagem.configure(state='normal')
    texto_da_imagem.delete('1.0', 'end')
    texto_da_imagem.insert('1.0', resultado)
    copiar_texto.configure(state='normal')
    texto_da_imagem.configure(state='disabled')


nova_captura = ttk.Button(text='Nova captura',
                          command=screenshot_cut)
nova_captura.pack(padx=10, pady=10, fill='both', expand='yes')

texto_da_imagem = Text(
    height=20,
    width=100,
    font=(None, 15),
    state='disabled'
)
texto_da_imagem.pack(padx=10, pady=10, fill='both', expand='yes')

def copiar_texto_f():
    janela.clipboard_clear()
    janela.clipboard_append(texto_da_imagem.get('1.0', 'end'))
    copiar_texto.configure(state='disabled')

copiar_texto = ttk.Button(text='Copiar texto',
                          command=copiar_texto_f,
                          state='disabled')
copiar_texto.pack(padx=10, pady=10, fill='both', expand='yes')


janela.mainloop()