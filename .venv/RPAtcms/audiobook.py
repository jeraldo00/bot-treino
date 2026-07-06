import pyttsx3
import PyPDF2

# === CONFIGURAÇÃO ===
pdf_file = r'C:\Users\jose.meireles\Desktop\Download\Apostila SQL Impressionador.pdf'     # Nome do PDF
audio_file = 'sql.mp3'  # Nome do MP3 gerado

# === LER O PDF ===
text = ""
with open(pdf_file, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() + "\n"

# === CONVERTER TEXTO EM ÁUDIO ===
engine = pyttsx3.init()
engine.save_to_file(text, audio_file)
engine.runAndWait()

print(f"Áudio gerado: {audio_file}")
