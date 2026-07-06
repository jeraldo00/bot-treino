import pyttsx3
import PyPDF2
import os
import difflib
import textwrap

# === CONFIGURAÇÃO FIXA ===
BASE_PATH = r"C:\Users\jose.meireles\Desktop\Download"
BLOCK_SIZE = 800  # quantidade de caracteres por bloco (ajustável para PDFs grandes)

# === SOLICITA O NOME DO ARQUIVO PDF (PARCIAL) ===
busca = input("Digite parte do nome do arquivo PDF: ").strip().lower()

# === LISTA TODOS OS PDFs DA PASTA ===
pdfs = [f for f in os.listdir(BASE_PATH) if f.lower().endswith('.pdf')]

# === PROCURA POR NOMES SEMELHANTES ===
encontrados = [f for f in pdfs if busca in f.lower()]

if not encontrados:
    print("❌ Nenhum arquivo encontrado.")
    exit()
elif len(encontrados) == 1:
    pdf_nome = encontrados[0]
else:
    print("🔍 Vários arquivos encontrados:")
    for i, nome in enumerate(encontrados, 1):
        print(f"[{i}] {nome}")
    opcao = input("Digite o número do arquivo desejado: ").strip()
    if not opcao.isdigit() or int(opcao) < 1 or int(opcao) > len(encontrados):
        print("🚫 Opção inválida. Encerrando.")
        exit()
    pdf_nome = encontrados[int(opcao)-1]

# === CONFIRMAÇÃO ===
confirm = input(f"\nVocê quer converter o livro '{pdf_nome}' para áudio com voz natural offline? (s/n): ").strip().lower()
if confirm != 's':
    print("🚫 Conversão cancelada.")
    exit()

# === CAMINHOS ===
pdf_file = os.path.join(BASE_PATH, pdf_nome)
audio_file = os.path.join(BASE_PATH, os.path.splitext(pdf_nome)[0] + ".mp3")

# === LER O PDF ===
print("\n📖 Lendo o arquivo PDF...")
text = ""
with open(pdf_file, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

if not text.strip():
    print("⚠️ O PDF não contém texto reconhecível.")
    exit()

# === CONFIGURAR PYTTSX3 PARA VOZ NATURAL ===
engine = pyttsx3.init()

# Lista vozes disponíveis
voices = engine.getProperty('voices')
print("\n🔊 Voices disponíveis:")
for i, v in enumerate(voices):
    print(f"[{i}] {v.name} - {v.id}")

# Permite escolher a voz
choice = input("\nDigite o número da voz desejada (ou Enter para padrão): ").strip()
if choice.isdigit() and int(choice) < len(voices):
    engine.setProperty('voice', voices[int(choice)].id)

# Ajusta velocidade e volume para mais naturalidade
engine.setProperty('rate', 160)    # padrão ~200, diminuir para mais natural
engine.setProperty('volume', 1.0)  # 0.0 a 1.0

# === DIVIDIR TEXTO EM BLOCO PARA LEITURA MAIS FLUIDA ===
blocks = textwrap.wrap(text, BLOCK_SIZE, break_long_words=False, replace_whitespace=False)

print(f"\n🎧 Convertendo texto em áudio offline em {len(blocks)} blocos...")

for i, block in enumerate(blocks, 1):
    print(f"🔹 Processando bloco {i}/{len(blocks)}...")
    engine.save_to_file(block, audio_file if i == 1 else audio_file)  # escreve no mesmo arquivo
    engine.runAndWait()

print(f"\n✅ Conversão concluída com sucesso!")
print(f"💾 Áudio salvo em: {audio_file}")
