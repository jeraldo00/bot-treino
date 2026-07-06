from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By

import time, os

from config import URL_SISTEMA, USUARIO, SENHA
import locators as loc

def iniciar_driver():
    caminho_driver = os.path.join("drivers", "chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    return webdriver.Chrome(service=Service(caminho_driver), options=options)

def fazer_login(driver):
    print("[INFO] Acessando sistema...")
    driver.get(URL_SISTEMA)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located(loc.CAMPO_USUARIO)).send_keys(USUARIO)
    driver.find_element(*loc.CAMPO_SENHA).send_keys(SENHA)
    driver.find_element(*loc.BOTAO_ACESSAR).click()
    print("[INFO] Login realizado com sucesso.")

def acessar_pesquisa_planos(driver):
    print("[INFO] Acessando menu de pesquisa...")

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(loc.MENU_PESQUISA)).click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(loc.SUBMENU_PLANOS_TESTE)).click()

    print("[INFO] Página 'Pesquisar Planos de Teste' acessada com sucesso.")

def editar_nome_e_salvar(driver):
    print("[INFO] Abrindo menu de opções do caso...")
    botoes_dropdown = driver.find_elements(By.XPATH, "//a[contains(@class, 'dropdown-toggle')]")

    for botao in botoes_dropdown:
        if 'fa-cogs' in botao.get_attribute("innerHTML"):
            driver.execute_script("arguments[0].click();", botao)
            break

    print("[INFO] Clicando na opção 'Editar'...")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Editar"))).click()

    print("[INFO] Editando nome do caso...")
    campo_nome = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_name")))
    nome_atual = campo_nome.get_attribute("value")
    primeira_palavra = nome_atual.split(" ")[0]
    novo_nome = nome_atual.replace(primeira_palavra, f"[{primeira_palavra}]")
    campo_nome.clear()
    campo_nome.send_keys(novo_nome)

    print(f"[INFO] Novo nome: {novo_nome}")

    print("[INFO] Salvando alteração...")
    botao_salvar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Salvar')]")
    ))
    driver.execute_script("arguments[0].scrollIntoView(true);", botao_salvar)
    time.sleep(1)
    botao_salvar.click()
    print("[SUCESSO] Caso editado e salvo com sucesso.\n")

    time.sleep(2)

    # Retornar para a listagem via menu "Pesquisa"
    acessar_pesquisa_planos(driver)
    time.sleep(2)


def procurar_e_abrir_casos_com_r(driver):
    while True:
        print("[INFO] Vasculhando casos na página atual...")

        links = [
            link for link in driver.find_elements(By.XPATH, "//a")
            if link.text.strip() != "" and link.text.strip().startswith("R")
        ]

        if not links:
            print("[INFO] Nenhum caso com 'R' nesta página.")
        else:
            for link in links:
                try:
                    caso = link.text.strip()
                    print(f"[ENCONTRADO] Caso encontrado: '{caso}'. Clicando para abrir...")

                    driver.execute_script("arguments[0].scrollIntoView(true);", link)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", link)

                    print(f"[INFO] Caso '{caso}' aberto com sucesso.")
                    time.sleep(3)
                    editar_nome_e_salvar(driver)

                    
                except Exception as e:
                    print(f"[ERRO] Erro ao abrir ou editar caso '{caso}':", e)

        try:
            botao_proximo = driver.find_element(By.XPATH, "//span[contains(@class, 'fa-angle-right')]/ancestor::a")
            driver.execute_script("arguments[0].scrollIntoView(true);", botao_proximo)
            time.sleep(0.5)
            botao_proximo.click()
            time.sleep(2)
        except NoSuchElementException:
            print("[FIM] Nenhuma próxima página encontrada. Encerrando busca.")
            break


def main():
    print("[INÍCIO] Executando robô...\n")
    driver = iniciar_driver()
    try:
        fazer_login(driver)
        acessar_pesquisa_planos(driver)
        time.sleep(3)
        procurar_e_abrir_casos_com_r(driver)
    except TimeoutException as e:
        print("[ERRO] Timeout ao tentar acessar algum elemento:", e)
    finally:
        print("\n[INFO] Encerrando robô.")
        driver.quit()

if __name__ == "__main__":
    main()
