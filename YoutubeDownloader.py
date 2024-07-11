import tkinter as tk
from tkinter import messagebox, ttk
from pydub import AudioSegment
import os
from pathlib import Path
from yt_dlp import YoutubeDL

def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes')
        downloaded_bytes = d.get('downloaded_bytes')
        percentage_of_completion = (downloaded_bytes / total_bytes) * 100
        progress_bar['value'] = percentage_of_completion
        root.update_idletasks()

def download_video(url):
    save_path = Path.home() / "Downloads"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(save_path / '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        messagebox.showinfo("Sucesso", "Download completo!")
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
