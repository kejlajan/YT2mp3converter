import os
from pytube import YouTube
from pydub import AudioSegment
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import sys
from io import StringIO



def get_filenames(dir_path = "./music/mp4", ext = 'mp4'):
    names = []
    for filename in os.listdir(dir_path):
        if filename.split('.')[-1] == ext:
            names.append(filename.split('.')[-2])
    
    return names




def get_overflowing_mp4s(mp4_dir = "./music/mp4", mp3_dir = "./music/mp3/"):
    mp4s = get_filenames(mp4_dir, ext="mp4")
    mp3s = get_filenames(mp3_dir, ext="mp3")
    
    over = []
    for filename in mp4s:
        if filename not in mp3s:
            over.append(filename)
    return over




def get_overflowing_URLs(URLs: list[str], download_dir_path = "./music/mp4/"):
    names = get_filenames(download_dir_path, ext="mp4")
    over = []
    for URL in URLs:
        if YouTube(URL).title not in names:
            over.append(URL)
    return over        




def download_sound_from_youtube_video(url, filepath):
    try:
        # Create a YouTube object with the URL
        yt = YouTube(url)
        
        # Get the highest resolution stream available
        stream = yt.streams.get_audio_only()
        
        # Download the video to the specified file path
        stream.download(output_path=filepath)
        
        print(f"Downloaded '{yt.title}' successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")




def download_music_from_urls(list_of_URLs: list[str], filepath = "./music/mp4/"):
    pocet = len(list_of_URLs)
    for index, URL in enumerate(list_of_URLs):
        download_sound_from_youtube_video(URL,filepath=filepath)
        print(f"{index+1}. video stazeno z adresy: {URL}")
    print(f"vse stazene z YT najdete ve slozce {filepath}")




def download_overflowing(URL_filepath = "./adresy.txt", output_dir_path_mp4="./music/mp4/"):
        with open(URL_filepath, 'r') as file:
            potential_URLs = [ line.strip() for line in file.readlines() ]
        try:
            URLs = get_overflowing_URLs(potential_URLs, download_dir_path=output_dir_path_mp4)
        except Exception as e:
            print(f"Ouha, nastala chyba: {e}")
        try:
            download_music_from_urls(URLs, filepath=output_dir_path_mp4)
        except Exception as e:
            print(f"Ouha, nastala chyba: {e}")


### Convert:



def convert_to_mp3(input_filename_path: str, output_dir = "./music/mp3/"):
    audio = AudioSegment.from_file(input_filename_path, format="mp4")
    print(f"converting into: {output_dir}{input_filename_path.split('.')[-2].split('/')[-1]}.mp3")
    audio.export(f"{output_dir}{input_filename_path.split('.')[-2].split('/')[-1]}.mp3", format = "mp3")
    print(f"CONVERTED into: {output_dir}{input_filename_path.split('.')[-2].split('/')[-1]}.mp3")




def convert_overflowing(input_dir="./music/mp4/", output_dir="./music/mp3/"):
    to_be_converted = get_overflowing_mp4s(mp4_dir=input_dir, mp3_dir=output_dir)
    
    for name in get_overflowing_mp4s(mp4_dir=input_dir, mp3_dir=output_dir):
        try:
            convert_to_mp3(f"{input_dir}{name}.mp4", output_dir=output_dir)
        except Exception as e:
            print(f"Ouha, nastala chyba: {e}")
    print(f"Vsech {len(to_be_converted)} souboru prekonvertovano nebo u nich nastala chyba.")
    print("Soubory ktere byly oznaceny ke konverzi:")
    print(to_be_converted)




def download_and_convert(URLs_filepath = "./adresy.txt", mp4_dirpath = "./music/mp4/", mp3_dirpath="./music/mp3/"):
    download_overflowing(URL_filepath=URLs_filepath, output_dir_path_mp4=mp4_dirpath)
    convert_overflowing(input_dir=mp4_dirpath, output_dir=mp3_dirpath)


### vytvorit adresarovou strukturu:



def create_directories_and_file():
    # Define the directory paths
    mp3_dir = Path("./music/mp3/")
    mp4_dir = Path("./music/mp4/")
    file_path = Path("./adresy.txt")

    # Create the directories if they do not exist
    mp3_dir.mkdir(parents=True, exist_ok=True)
    mp4_dir.mkdir(parents=True, exist_ok=True)

    # Create the file if it does not exist
    if not file_path.exists():
        file_path.touch()

    print(f"Directories '{mp3_dir}' and '{mp4_dir}' created or already exist.")
    print(f"File '{file_path}' created or already exists.")




create_directories_and_file()




class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

def select_mp3_slozka():
    mp3_slozka_path = filedialog.askdirectory()
    if mp3_slozka_path:
        mp3_slozka_entry.delete(0, tk.END)
        mp3_slozka_entry.insert(0, mp3_slozka_path)

def select_mp4_slozka():
    mp4_slozka_path = filedialog.askdirectory()
    if mp4_slozka_path:
        mp4_slozka_entry.delete(0, tk.END)
        mp4_slozka_entry.insert(0, mp4_slozka_path)

def select_soubor_adres_URL():
    soubor_adres_URL_path = filedialog.askopenfilename()
    if soubor_adres_URL_path:
        soubor_adres_URL_entry.delete(0, tk.END)
        soubor_adres_URL_entry.insert(0, soubor_adres_URL_path)

def launch_download():
    print("Stahuji")
    mp3_slozka = mp3_slozka_entry.get()
    mp4_slozka = mp4_slozka_entry.get()
    soubor_adres_URL = soubor_adres_URL_entry.get()
    download_and_convert(URLs_filepath=soubor_adres_URL, mp4_dirpath=mp4_slozka+'/', mp3_dirpath=mp3_slozka+'/')
    print(f"Hudba je v: {mp3_slozka}")
    print(f"MP4 je v: {mp4_slozka}")
    print(f"Soubor Adres URL je v: {soubor_adres_URL}")

# Create the main window
root = tk.Tk()
root.title("Directory and File Selector")

# Default values
default_mp3_slozka = "./music/mp3"
default_mp4_slozka = "./music/mp4"
default_soubor_adres_URL = "./adresy.txt"

# MP3 Složka
mp3_slozka_label = tk.Label(root, text="MP3 Složka:")
mp3_slozka_label.grid(row=0, column=0, padx=10, pady=10)
mp3_slozka_entry = tk.Entry(root, width=50)
mp3_slozka_entry.grid(row=0, column=1, padx=10, pady=10)
mp3_slozka_entry.insert(0, default_mp3_slozka)  # Set default value
mp3_slozka_button = tk.Button(root, text="Browse", command=select_mp3_slozka)
mp3_slozka_button.grid(row=0, column=2, padx=10, pady=10)

# MP4 Složka
mp4_slozka_label = tk.Label(root, text="MP4 Složka:")
mp4_slozka_label.grid(row=1, column=0, padx=10, pady=10)
mp4_slozka_entry = tk.Entry(root, width=50)
mp4_slozka_entry.grid(row=1, column=1, padx=10, pady=10)
mp4_slozka_entry.insert(0, default_mp4_slozka)  # Set default value
mp4_slozka_button = tk.Button(root, text="Browse", command=select_mp4_slozka)
mp4_slozka_button.grid(row=1, column=2, padx=10, pady=10)

# Soubor Adres URL
soubor_adres_URL_label = tk.Label(root, text="Soubor Adres URL:")
soubor_adres_URL_label.grid(row=2, column=0, padx=10, pady=10)
soubor_adres_URL_entry = tk.Entry(root, width=50)
soubor_adres_URL_entry.grid(row=2, column=1, padx=10, pady=10)
soubor_adres_URL_entry.insert(0, default_soubor_adres_URL)  # Set default value
soubor_adres_URL_button = tk.Button(root, text="Browse", command=select_soubor_adres_URL)
soubor_adres_URL_button.grid(row=2, column=2, padx=10, pady=10)

# OK Button
ok_button = tk.Button(root, text="OK", command=launch_download)
ok_button.grid(row=3, column=0, columnspan=3, pady=10)

# Frame for text widget and scrollbar
text_frame = tk.Frame(root)
text_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Text widget for standard output
stdout_text = tk.Text(text_frame, wrap=tk.WORD, height=10, width=80)
stdout_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the text widget
scrollbar = tk.Scrollbar(text_frame, command=stdout_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
stdout_text.config(yscrollcommand=scrollbar.set)

# Redirect stdout to the text widget
sys.stdout = StdoutRedirector(stdout_text)

# Run the application
root.mainloop()

