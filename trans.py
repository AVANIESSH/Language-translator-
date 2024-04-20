""" Real Time Multimodal Translator."""
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox
import os
import googletrans
import textblob
from gtts import gTTS
from playsound import playsound
from PIL import Image, ImageTk
import pytesseract
import speech_recognition as sr
import easyocr

class Run:
    """This class represents the Language Translator application."""
    def __init__(self):
        # GUI Screen
        self.root = tk.Tk()
        self.root.title("Language - Translator")
        self.root.geometry("1040x500")  # Increased the height to accommodate image display
        self.root.resizable(False, False)
        self.root.config(bg='#b2c2cf')
        self.top_frame = tk.Frame(self.root, bg="white", width=1020, height=15)
        self.top_frame.place(x=0, y=0)
        # Calling Widgets Function
        self.placing_widgets()
        self.root.mainloop()
        self.reco = None
        self.text = None
        
    def placing_widgets(self):
        """GUI"""
        # Language List
        self.languages = googletrans.LANGUAGES
        self.language_list = list(self.languages.values())
        # Text Boxes
        self.original_text = tk.Text(
            self.root, height=10, width=40, bg="#ffffff", font=("Times New Roman", 15))
        self.original_text.grid(row=1, column=1, pady=20, padx=10, rowspan=3)
        self.translated_text = tk.Text(
            self.root, height=10, width=40, bg="#ffffff", font=("Times New Roman", 15))
        self.translated_text.grid(row=1, column=3, pady=20, padx=10, rowspan=3)
        # Buttons
        self.translated_button = tk.Button(self.root, text="Translate!", font=(
            "Helvetica", 20), command=self.translate_it, bg="#4db4d6", fg="black")
        self.translated_button.grid(row=2, column=2, padx=15)
        self.input_button = tk.Button(self.root, text="Voice_input", font=(
            "Helvetica", 20), command=self.input, bg='#4db4d6')
        self.input_button.grid(row=12, column=1, padx=10)
        self.translated_button = tk.Button(self.root, text="Voice_output", font=(
            "Helvetica", 20), command=self.speak, bg='#4db4d6')
        self.translated_button.grid(row=12, column=3, padx=10)
        self.image_button = tk.Button(self.root, text="Load Image", font=(
            "Helvetica", 20), command=self.load_image, bg='#4db4d6')
        self.image_button.grid(row=12, column=2, padx=10)
        # combo Boxes
        self.original_combo = ttk.Combobox(
            self.root, width=50, value=self.language_list)
        self.original_combo.current(21)
        self.original_combo.grid(row=6, column=1)

        self.translated_combo = ttk.Combobox(
            self.root, width=50, value=self.language_list)
        self.translated_combo.current(38)
        self.translated_combo.grid(row=6, column=3)
        # clear Button
        self.clear_btn = tk.Button(
            self.root, text="Clear", command=self.clear, bg='#4db4d6', width=6, height=2)
        self.clear_btn.grid(row=3, column=2)
        # Image display
        self.image_label = tk.Label(self.root, bg='white')
        self.image_label.grid(row=1, column=4, rowspan=3)
    # Translation
    def translate_it(self):
        """Translate text from the original language to the selected language."""
        self.translated_text.delete(1.0, tk.END)
        try:
            for key, value in self.languages.items():
                if value == self.original_combo.get():
                    from_language_key = key
            for key, value in self.languages.items():
                if value == self.translated_combo.get():
                    to_language_key = key
            words = textblob.TextBlob(self.original_text.get(1.0, tk.END))
            words = words.translate(
                from_lang=from_language_key, to=to_language_key)
            self.translated_text.insert(1.0, words)
        except FileNotFoundError as exception:
            messagebox.showerror("Translator", exception)
    # Taking Input From Mic
    def input(self):
        """Capture voice input and display it in the original_text box."""
        for key, value in self.languages.items():
            if value == self.original_combo.get():
                from_language_key = key
        #import speech_recognition as sr
        self.reco = sr.Recognizer()
        with sr.Microphone() as source:
            self.reco.adjust_for_ambient_noise(source, duration=0.3)
            print("Speak now")
            audio = self.reco.listen(source)
            try:
                self.text = self.reco.recognize_google(
                    audio, language=from_language_key)
                self.original_text.insert(1.0, self.text)
            except sr.UnknownValueError:
                messagebox.showerror('Not Recognized', 'No speech detected. Please try again.')
            except sr.RequestError as e:
                messagebox.showerror('Request Error', f'Error making a request to the recognition service: {e}')
    # Output Through Speaker
    def speak(self):
        """Convert translated text to speech and play it."""
        for key, value in self.languages.items():
            if value == self.translated_combo.get():
                to_language_key = key
        words = self.translated_text.get(1.0, tk.END)
        # Converting text into a mp3 File
        obj = gTTS(text=words, slow=False, lang=to_language_key)
        obj.save('captured_voice.mp3')

        # Playing the converted mp3 File
        playsound("E:\\projects\\captured_voice.mp3")
        # Removing the mp3 File After Playing
        os.remove("E:\\projects\\captured_voice.mp3")
    # Load Image and extract text
    def load_image(self):
        """Load an image, extract text, and display it in the original_text box."""
        pytesseract.pytesseract.tesseract_cmd=r'C:\Users\LENOVO\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                self.original_text.delete(1.0, tk.END)
                self.original_text.insert(1.0, text)
                # Display the loaded image
                image = Image.open(file_path)
                image = image.resize((200, 200), Image.LANCZOS)  
                image = ImageTk.PhotoImage(image)
                self.image_label.config(image=image)
                self.image_label.image = image
            except FileNotFoundError as fnfe:
                messagebox.showerror("Error", f"File not found: {fnfe}")
            except PermissionError as pe:
                messagebox.showerror("Error", f"Permission denied: {pe}")
            #except Exception as exception:
                #messagebox.showerror("Error", f"Error loading image: {exception}")
    # Clearing All The Inputed And Outputed Text
    def clear(self):
        """Clear the content of both text boxes."""
        self.original_text.delete(1.0, tk.END)
        self.translated_text.delete(1.0, tk.END)
# Creating Object
my_run_instance = Run()


