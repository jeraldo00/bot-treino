import pyttsx3
import PyPDF2
import os

# === SOLICITA O CAMINHO DO PDF ===
pdf_file = input("Digite o caminho completo do arquivo PDF a ser convertido: ").strip()

# === GERA NOME AUTOMÁTICO PARA O ÁUDIO ===
# Exemplo: "C:\pasta\arquivo.pdf" -> "arquivo.mp3"
audio_file = os.path.splitext(os.path.basename(pdf_file))[0] + ".mp3"

# === LER O PDF ===
text = ""
try:
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
except FileNotFoundError:
    print("❌ Arquivo não encontrado. Verifique o caminho e tente novamente.")
    exit()

# === CONVERTER TEXTO EM ÁUDIO ===
print("🎧 Convertendo texto em áudio... isso pode levar alguns minutos...")
engine = pyttsx3.init()
engine.save_to_file(text, audio_file)
engine.runAndWait()

print(f"✅ Conversão concluída! O áudio foi gerado como: {audio_file}")
