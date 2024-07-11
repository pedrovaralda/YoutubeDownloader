# Descrição
Este script Python cria uma aplicação GUI (Graphical User Interface) que permite aos usuários baixar vídeos do YouTube e convertê-los para o formato MP3. 
O download é iniciado automaticamente quando o usuário insere um link do YouTube e pressiona Enter. O arquivo MP3 é salvo na pasta "Downloads" do computador do usuário.

# Bibliotecas Utilizadas
1. tkinter: Usada para criar a interface gráfica do usuário.
2. yt-dlp: Utilizada para baixar vídeos do YouTube.
3. pydub: Utilizada para converter o áudio do vídeo para o formato MP3.
4. os: Usada para manipulação de arquivos e diretórios.
5. pathlib: Utilizada para facilitar a manipulação de caminhos de arquivos e diretórios.

# Pré-requisitos
- Python 3.x
- As bibliotecas yt-dlp, pydub, e tkinter devem estar instaladas.
- O ffmpeg deve estar instalado e configurado no PATH do sistema.

# Instalando as bibliotecas necessárias
```sh
pip install yt-dlp pydub
```

# Instalando o ffmpeg
- As instruções de instalação do ffmpeg podem ser encontradas no site oficial [Ffmpeg](https://ffmpeg.org/download.html).

# Estrutura do Código
### Importação das Bibliotecas

```sh
import tkinter as tk
from tkinter import messagebox, ttk
from pydub import AudioSegment
import os
from pathlib import Path
from yt_dlp import YoutubeDL
```

### Função de Callback do Progresso
Esta função atualiza a barra de progresso durante o download do vídeo.

```sh
def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes')
        downloaded_bytes = d.get('downloaded_bytes')
        percentage_of_completion = (downloaded_bytes / total_bytes) * 100
        progress_bar['value'] = percentage_of_completion
        root.update_idletasks()
```

### Função para Download do Vídeo
Esta função baixa o vídeo do YouTube e o converte para MP3, salvando o arquivo na pasta "Downloads".

```sh
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
```

### Função para Detecção de Mudança no Campo de Entrada
Esta função é chamada quando o conteúdo do campo de entrada muda. Se o URL não estiver vazio, a função download_video é chamada.

```sh
def on_entry_change(*args):
    url = url_entry.get()
    if url:
        download_video(url)
```

### Criação da Interface Gráfica
Esta parte do código cria a interface gráfica usando tkinter.

```sh
root = tk.Tk()
root.title("YouTube to MP3 Downloader")

tk.Label(root, text="URL do YouTube:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

url_entry.bind("<Return>", lambda event: on_entry_change())

root.mainloop()
```

# Como Usar
1. Execute o script Python.
2. Insira um link do YouTube no campo de entrada.
3. Pressione Enter.
4. O vídeo será baixado e convertido para MP3 automaticamente.
5. O arquivo MP3 será salvo na pasta "Downloads" do seu computador.

# Considerações Finais
- Certifique-se de que o ffmpeg está corretamente instalado e configurado no PATH do seu sistema para que a conversão para MP3 funcione.
- O programa exibe uma barra de progresso durante o download para informar o usuário sobre o andamento do processo.
- Se ocorrer algum erro durante o download ou conversão, uma mensagem de erro será exibida.
