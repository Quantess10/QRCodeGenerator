import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
import qrcode
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageTk
import io

global qr_label
qr_label = None
global barcode_label
barcode_label = None

def resource_path(relative_path):
    """ Zwraca ścieżkę do zasobów wewnątrz skompilowanego pliku .exe lub w normalnym środowisku."""
    try:
        # Ścieżki dla skompilowanej aplikacji
        base_path = sys._MEIPASS
    except Exception:
        # Ścieżki dla środowiska deweloperskiego
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def center_window(window, width, height):
    # Pobierz wymiary ekranu
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Oblicz pozycję x i y, aby okno było na środku
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

def validate_length(action, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
    # action 1 = insert, 0 = delete
    if action == '1':  # Tylko przy wstawianiu tekstu
        # Sprawdź, czy po wstawieniu długość tekstu nie przekroczy 13 znaków
        total_length = len(prior_value) + len(text)
        if total_length > 13:
            messagebox.showwarning("Ostrzeżenie", "Kod kreskowy może zawierać maksymalnie 13 cyfr.")
            return False  # Blokada wstawienia tekstu
    return True

def on_focus_in_qr(event):
    if text_windowqr.get() == 'Wpisz tekst tutaj...':
        text_windowqr.delete(0, tk.END)
        text_windowqr.config()

def on_focus_out_bar(event):
    if text_windowbar.get() == '':
        text_windowbar.insert(0, 'Wpisz tekst tutaj...')
        text_windowbar.config()    

def on_focus_in_bar(event):
    if text_windowbar.get() == 'Wpisz tekst tutaj...':
        text_windowbar.delete(0, tk.END)
        text_windowbar.config()

def on_focus_out_qr(event):
    if text_windowqr.get() == '':
        text_windowqr.insert(0, 'Wpisz tekst tutaj...')
        text_windowqr.config()            

def generate_qr():
    # Pobranie tekstu z pola tekstowego
    global qr_label
    text = text_windowqr.get()
    if text == '' or text == 'Wpisz tekst tutaj...':
        messagebox.showinfo("Error! Error! Dziura w samolocie!", "Nie wygeneruję Ci kodu z niczego! Wpisz coś :)")
        return
    
    if qr_label is not None:
        qr_label.destroy()
    
    # Generowanie kodu QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Konwersja obrazu PIL do formatu Tkinter
    img_tk = ImageTk.PhotoImage(img)
    
    # Wyświetlenie obrazu kodu QR w aplikacji (możesz potrzebować dodatkowej ramki lub canvasa)
    qr_label = ttk.Label(frame_qrgenerator, image=img_tk)
    qr_label.image = img_tk  # trzymaj referencję!
    qr_label.pack(pady=10)  

def generate_barcode():
    global barcode_label
    # Pobranie tekstu z pola tekstowego
    text = text_windowbar.get()
    if len(text) != 13:
        messagebox.showwarning("Ostrzeżenie", "Kod kreskowy musi składać się z 13 cyfr.")
        return
    if text == '' or text == 'Wpisz tekst tutaj...':
        messagebox.showinfo("Error! Error! Dziura w samolocie!", "Nie wygeneruję Ci kodu z niczego! Wpisz coś :)")
        return

    if barcode_label is not None:
        barcode_label.destroy()

    # Wybór typu kodu kreskowego, np. EAN13, UPC, ISBN
    barcode_class = barcode.get_barcode_class('EAN13')
    
    # Generowanie kodu kreskowego
    try:
        barcode_obj = barcode_class(text, writer=ImageWriter())
    except barcode.errors.IllegalCharacterError:
        messagebox.showerror("Błąd", "Nieprawidłowe dane. Wpisz 13 cyfrowy kod!")
        return
    except ValueError as e:
        messagebox.showerror("Błąd", str(e))
        return

    # Generowanie obrazu kodu kreskowego do strumienia w pamięci
    barcode_io = io.BytesIO()
    barcode_obj.write(barcode_io)
    barcode_io.seek(0)

    # Ładowanie obrazu kodu kreskowego
    img = Image.open(barcode_io)
    img_tk = ImageTk.PhotoImage(img)

    # Wyświetlenie obrazu kodu kreskowego w aplikacji
    barcode_label = ttk.Label(frame_barcodegenerator, image=img_tk)
    barcode_label.image = img_tk  # trzymaj referencję!
    barcode_label.pack(pady=10)    

def init_welcome_frame():
    global welcome_frame
    global label
    welcome_frame = ttk.Frame(root)
    welcome_frame.pack()

    # Załaduj obraz
    image_path = resource_path('main_image.jpg')
    image = Image.open(image_path)
    image = image.resize((500, 500))
    photo = ImageTk.PhotoImage(image)

    # Utwórz etykietę z obrazem
    label = ttk.Label(welcome_frame, image=photo)
    label.image = photo  # Trzymaj referencję do obrazu
    label.pack()  # Możesz dodać pady lub padx, aby ustawić marginesy

def init_qrgenerator_frame():
    global frame_qrgenerator
    global text_windowqr
    frame_qrgenerator = ttk.Frame(root)
    qr_title = ttk.Label(frame_qrgenerator, text="Generator kodów QR")
    qr_title.pack()

    text_windowqr = ttk.Entry(frame_qrgenerator, width=70)
    text_windowqr.insert(0, 'Wpisz tekst tutaj...')
    text_windowqr.bind('<FocusIn>', on_focus_in_qr)
    text_windowqr.bind('<FocusOut>', on_focus_out_qr)
    text_windowqr.pack(side=tk.TOP, anchor=tk.CENTER, pady=10)
    
    button_generateqr = ttk.Button(frame_qrgenerator, text="Generuj kod QR", command=generate_qr, width=20)
    button_generateqr.pack(side=tk.TOP, anchor=tk.CENTER, pady=10)

def init_barcodegenerator_frame():
    global frame_barcodegenerator
    global text_windowbar
    frame_barcodegenerator = ttk.Frame(root)
    barcode_title = ttk.Label(frame_barcodegenerator, text="Generator kodów kreskowych")
    barcode_title.pack()

    text_windowbar = ttk.Entry(frame_barcodegenerator, width=70)
    text_windowbar.insert(0, 'Wpisz tekst tutaj...')
    text_windowbar.bind('<FocusIn>', on_focus_in_bar)
    text_windowbar.bind('<FocusOut>', on_focus_out_bar)
    text_windowbar.pack(side=tk.TOP, anchor=tk.CENTER, pady=10)
    
    button_generatebarcode = ttk.Button(frame_barcodegenerator, text="Generuj kod kreskowy", command=generate_barcode, width=20)
    button_generatebarcode.pack(side=tk.TOP, anchor=tk.CENTER, pady=10)    

def switch_view(view):
    # Ukryj wszystkie ramy
    welcome_frame.pack_forget()
    frame_qrgenerator.pack_forget()
    frame_barcodegenerator.pack_forget()
    
    # Pokaż wybraną ramę
    if view == 'start':
        welcome_frame.pack(fill=tk.BOTH, expand=True)   
    elif view == 'qrgenerator':
        frame_qrgenerator.pack(fill=tk.BOTH, expand=True)    

    elif view == 'barcodegenerator':
        frame_barcodegenerator.pack(fill=tk.BOTH, expand=True)      

root = ThemedTk(theme="adapta")
root.title("Generator kodów kreskowych i QR")
root.iconbitmap(resource_path('ikona.ico'))
center_window(root, 700, 500)

vcmd = (root.register(validate_length), '%d', '%S', '%s', '%i', '%V', '%T', '%W')
text_windowbar = ttk.Entry(root, validate="key", validatecommand=vcmd)

menu_frame = ttk.Frame(root)
menu_frame.pack(side=tk.LEFT, fill=tk.Y)

button_start = ttk.Button(menu_frame, text="Start", width=20, command=lambda: switch_view('start'))
button_start.pack(side=tk.TOP, anchor=tk.CENTER)
button_qrmenu = ttk.Button(menu_frame, text="Kod QR", width=20, command=lambda: switch_view('qrgenerator'))
button_qrmenu.pack(side=tk.TOP, anchor=tk.CENTER)
button_2dmenu = ttk.Button(menu_frame, text="Kod kreskowy", width=20, command=lambda: switch_view('barcodegenerator'))
button_2dmenu.pack(side=tk.TOP, anchor=tk.CENTER)


init_welcome_frame()
init_qrgenerator_frame()
init_barcodegenerator_frame()

root.mainloop()
