import tkinter as tk
from tkinter import messagebox, ttk
from pytube import YouTube
from pydub import AudioSegment
import os
from pathlib import Path

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = (bytes_downloaded / total_size) * 100
    progress_bar['value'] = percentage_of_completion
    root.update_idletasks()

def download_video(url):
    save_path = Path.home() / "Downloads"
    
    try:
        yt = YouTube(url, on_progress_callback=progress_function)
        video = yt.streams.filter(only_audio=True).first()
        download_path = video.download(output_path=save_path)
        
        base, ext = os.path.splitext(download_path)
        new_file = base + '.mp3'
        
        audio = AudioSegment.from_file(download_path)
        audio.export(new_file, format='mp3')
        
        os.remove(download_path)
        
        messagebox.showinfo("Sucesso", f"Download completo: {new_file}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def on_entry_change(*args):
    url = url_entry.get()
    if url:
        download_video(url)

# Interface gráfica
root = tk.Tk()
root.title("YouTube to MP3 Downloader")

tk.Label(root, text="URL do YouTube:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

url_entry.bind("<Return>", lambda event: on_entry_change())

root.mainloop()
