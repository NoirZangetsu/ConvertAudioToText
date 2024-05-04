import tkinter as tk
from tkinter import filedialog, messagebox
import speech_recognition as sr
from pydub import AudioSegment
import os

# pydub için ffmpeg ve ffprobe yollarını başlangıçta belirtin
AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"
AudioSegment.ffprobe = "/opt/homebrew/bin/ffprobe"

def sesi_metne_cevir(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        metin = recognizer.recognize_google(audio, language='tr-TR')
        metin_kutusu.delete(1.0, tk.END)
        metin_kutusu.insert(tk.END, metin)
    except sr.UnknownValueError:
        messagebox.showerror("Hata", "Ses algılanamadı.")
    except sr.RequestError as e:
        messagebox.showerror("Hata", f"Google API hatası: {e}")

def dosya_sec():
    dosya_yolu = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3")])
    if dosya_yolu:
        if dosya_yolu.lower().endswith('.mp3'):
            temp_path = os.path.splitext(dosya_yolu)[0] + "_temp.wav"
            sound = AudioSegment.from_mp3(dosya_yolu)
            sound.export(temp_path, format="wav")
            sesi_metne_cevir(temp_path)
            os.remove(temp_path)
        else:
            sesi_metne_cevir(dosya_yolu)

def metni_kaydet():
    metin = metin_kutusu.get(1.0, tk.END).strip()
    if metin:
        dosya_adı = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if dosya_adı:
            with open(dosya_adı, "w") as dosya:
                dosya.write(metin)
            messagebox.showinfo("Başarılı", "Metin dosyaya kaydedildi.")

def metni_kopyala():
    app.clipboard_clear()
    metin = metin_kutusu.get(1.0, tk.END)
    app.clipboard_append(metin)
    messagebox.showinfo("Kopyalandı", "Metin panoya kopyalandı.")

app = tk.Tk()
app.title("Ses Dosyasını Metne Çevir")

mainframe = tk.Frame(app)
mainframe.pack(padx=10, pady=10)

sec_dosya_btn = tk.Button(mainframe, text="Ses Dosyası Seç", command=dosya_sec)
sec_dosya_btn.pack(side=tk.TOP, fill=tk.X)

metin_kutusu = tk.Text(mainframe, height=10, width=50)
metin_kutusu.pack(pady=(5, 10))

kopyala_btn = tk.Button(mainframe, text="Metni Kopyala", command=metni_kopyala)
kopyala_btn.pack(side=tk.LEFT, fill=tk.X)

kaydet_btn = tk.Button(mainframe, text="Metni Kaydet", command=metni_kaydet)
kaydet_btn.pack(side=tk.RIGHT, fill=tk.X)

app.mainloop()
