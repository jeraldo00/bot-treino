import time
import requests
from bs4 import BeautifulSoup
from win10toast_click import ToastNotifier
import os
import webbrowser
import urllib3

# Desabilitar aviso de segurança SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lista de sites para monitorar (URL, seletor CSS para título)
SITES = [
    {
        "url": "https://www.estrategiaconcursos.com.br/blog/concurso-banco-do-brasil-ultimas-noticias/",
        "selector": "h1"
    },
    {
        "url": "https://blog.grancursosonline.com.br/concurso-banco-do-brasil/",
        "selector": "h1"
    },
    {
        "url": "https://www.novaconcursos.com.br/portal/concursos/concurso-banco-do-brasil/",
        "selector": "h1"
    },
    {
        "url": "https://www.direcaoconcursos.com.br/noticias/concurso-banco-do-brasil",
        "selector": "h1"
    }
]

ARQUIVO_CACHE = "ultima_noticia.txt"

# Função para pegar o título mais recente
def pegar_noticia():
    noticias = []
    for site in SITES:
        try:
            resp = requests.get(site["url"], timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resp.text, "html.parser")
            titulo = soup.select_one(site["selector"]).get_text(strip=True)
            noticias.append((titulo, site["url"]))
        except Exception as e:
            print(f"Erro ao acessar {site['url']}: {e}")
    return noticias

# Ler cache
def ler_cache():
    if os.path.exists(ARQUIVO_CACHE):
        with open(ARQUIVO_CACHE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

# Salvar cache
def salvar_cache(titulo):
    with open(ARQUIVO_CACHE, "w", encoding="utf-8") as f:
        f.write(titulo)

# Notificar com clique abrindo link
def notificar(mensagem, link):
    toaster = ToastNotifier()
    toaster.show_toast(
        "Concurso Banco do Brasil",
        mensagem,
        duration=10,
        callback_on_click=lambda: webbrowser.open(link)
    )

# Loop principal
def monitorar():
    print("🔍 Monitorando novidades do Concurso Banco do Brasil...")
    while True:
        noticias = pegar_noticia()
        ultima_cache = ler_cache()

        if noticias and noticias[0][0] != ultima_cache:
            titulo, link = noticias[0]
            notificar(f"Nova notícia: {titulo}", link)
            salvar_cache(titulo)
            print(f"🔔 Notificação enviada: {titulo}")
        else:
            print("Nenhuma novidade encontrada.")

        time.sleep(3600)  # verifica a cada 1 hora

if __name__ == "__main__":
    monitorar()
