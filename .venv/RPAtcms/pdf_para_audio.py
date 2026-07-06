import pyttsx3
import PyPDF2
import os
import difflib

# === CONFIGURAÇÃO FIXA ===
BASE_PATH = r"C:\Users\jose.meireles\Desktop\Download"

# === SOLICITA O NOME DO ARQUIVO PDF (PARCIAL) ===
busca = input("Digite parte do nome do arquivo PDF: ").strip().lower()

# === LISTA TODOS OS PDFs DA PASTA ===
pdfs = [f for f in os.listdir(BASE_PATH) if f.lower().endswith('.pdf')]

# === PROCURA POR NOMES SEMELHANTES ===
encontrados = [f for f in pdfs if busca in f.lower()]

if not encontrados:
    # Usa similaridade aproximada se não houver correspondência direta
    semelhantes = difflib.get_close_matches(busca, pdfs, n=3, cutoff=0.4)
    if semelhantes:
        print("🔍 Nenhum nome exato encontrado, mas encontrei algo parecido:")
        for s in semelhantes:
            print(f" - {s}")
        escolha = input("Digite o nome completo de um dos arquivos acima (ou pressione Enter para sair): ").strip()
        if not escolha:
            print("🚫 Nenhum arquivo selecionado. Encerrando.")
            exit()
        pdf_nome = escolha
    else:
        print("❌ Nenhum arquivo semelhante encontrado na pasta.")
        exit()
else:
    # Se encontrou um ou mais PDFs com o termo buscado
    if len(encontrados) == 1:
        pdf_nome = encontrados[0]
    else:
        print("🔍 Vários arquivos encontrados:")
        for i, nome in enumerate(encontrados, 1):
            print(f"[{i}] {nome}")
        opcao = input("Digite o número do arquivo desejado: ").strip()
        if not opcao.isdigit() or int(opcao) < 1 or int(opcao) > len(encontrados):
            print("🚫 Opção inválida. Encerrando.")
            exit()
        pdf_nome = encontrados[int(opcao) - 1]

# === CONFIRMAÇÃO ===
confirm = input(f"Você quer converter o livro '{pdf_nome}' para áudio? (s/n): ").strip().lower()
if confirm != 's':
    print("🚫 Conversão cancelada.")
    exit()

# === CAMINHOS DOS ARQUIVOS ===
pdf_file = os.path.join(BASE_PATH, pdf_nome)
audio_file = os.path.join(BASE_PATH, os.path.splitext(pdf_nome)[0] + ".mp3")

# === LER O PDF ===
text = ""
print("📖 Lendo o arquivo PDF...")

try:
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
except Exception as e:
    print(f"⚠️ Erro ao ler o arquivo PDF: {e}")
    exit()

# === CONVERTER TEXTO EM ÁUDIO ===
print("🎧 Convertendo texto em áudio... isso pode levar alguns minutos...")
engine = pyttsx3.init()
engine.save_to_file(text, audio_file)
engine.runAndWait()

print(f"✅ Conversão concluída com sucesso!")
print(f"💾 Arquivo gerado: {audio_file}")
