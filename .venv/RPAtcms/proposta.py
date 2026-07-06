from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

CAMINHO_CHROMEDRIVER = r"C:\\Users\\jose.meireles\\Desktop\\Automação\\.venv\\RPAtcms\\drivers\\chromedriver.exe"
service = Service(CAMINHO_CHROMEDRIVER)
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)
wait_modal = WebDriverWait(driver, 15)

def preencher_ion_input(name, valor):
    campo = wait.until(EC.presence_of_element_located((By.NAME, name)))
    driver.execute_script("""
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    """, campo, valor)
    time.sleep(0.5)

try:
    # 1. Abrir página de login
    driver.get("https://api-tst.brbcard.com.br/portalgerentestst")
    driver.maximize_window()

    # 2. Login
    cpf_ion_input = wait.until(EC.presence_of_element_located((By.XPATH, "(//ion-input)[1]")))
    senha_ion_input = wait.until(EC.presence_of_element_located((By.XPATH, "(//ion-input)[2]")))

    ActionChains(driver).move_to_element(cpf_ion_input).click().send_keys("02878465121").perform()
    time.sleep(1)
    ActionChains(driver).move_to_element(senha_ion_input).click().send_keys("cartao16").perform()
    time.sleep(1)

    driver.execute_script("document.getElementsByName('ion-input-0')[0].value = '02878465121';")
    driver.execute_script("document.getElementsByName('ion-input-1')[0].value = 'cartao16';")
    driver.execute_script("""
        let evt = new Event('input', { bubbles: true });
        document.getElementsByName('ion-input-0')[0].dispatchEvent(evt);
        document.getElementsByName('ion-input-1')[0].dispatchEvent(evt);
    """)
    time.sleep(1)

    botao_entrar = wait.until(EC.element_to_be_clickable((By.XPATH, "//ion-button[contains(., 'Acessar')]")))
    botao_entrar.click()
    print("Login tentado com sucesso.")
    time.sleep(5)

    # 3. Clicar no radio "acompanhar-propostas"
    driver.execute_script("""
        const radio = document.querySelector('ion-radio[value="acompanhar-propostas"]');
        if (radio) { radio.click(); }
    """)
    print("Radio 'acompanhar-propostas' clicado.")
    time.sleep(3)

    # 4. Clicar no botão "Solicitar cartão"
    botao_solicitar = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//ion-button[.//ion-label[contains(text(), 'Solicitar cartão')]]"))
    )
    botao_solicitar.click()
    print("Botão 'Solicitar cartão' clicado.")
    time.sleep(1)

    # 5. Esperar o modal de CPF aparecer
    print("Esperando modal CPF...")
    modal_cpf = wait_modal.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "ion-modal.cpfSolicitarCartao.show-modal"))
    )
    print("Modal CPF visível.")

    cpf_input = wait_modal.until(
    EC.element_to_be_clickable((By.XPATH, "//app-brbcard-modal-solicitar-cartao//form//ion-input//input"))
    )
    cpf_input.clear()
    cpf_input.click()
    cpf_input.send_keys("94237841006")
    print("CPF preenchido no modal.")

        # 6. Selecionar conta "Puro Crédito"
    # Espera e clica no seletor da conta (abre o popover)
    seletor_conta = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//ion-select[@formcontrolname='contaCorrente']"))
    )
    seletor_conta.click()
    print("Seletor de conta clicado.")

    # 2. Espera o popover com as opções aparecer
    # Esperar o popover carregar e pegar o item "Puro Crédito"
    # element = wait.until(
    # EC.element_to_be_clickable((By.XPATH, '//*[@id="ion-rb-34-lbl"]'))
    # )
    try:
        time.sleep(5)
        element = driver.find_element(By.XPATH, '//ion-radio[@aria-labelledby="ion-rb-4-lbl"]')
        element.click()
        print(element.text.strip())
        
        # html_completo = driver.page_source
        #with open('pagina.html', 'w', encoding='utf-8') as f:
        #    f.write(html_completo)
        #host = driver.find_element(By.CSS_SELECTOR, 'ion-select')  # substitua pelo host real
        #shadow_root = driver.execute_script('return arguments[0].shadowRoot', host)
        #element = shadow_root.find_element(By.CSS_SELECTOR, '#ion-rb-36-lbl')
        #print(element.text.strip())
        
    except AssertionError as e:
        print(e)
        
    # driver.execute_script("arguments[0].click();", element)
    print("Clique no elemento via XPath executado.")

    # Esperar o modal desaparecer
    wait.until(EC.invisibility_of_element(modal_cpf))
    print("Modal CPF fechado.")

    # 8. Esperar tela mudar e clicar no botão após mudança
    # O botão descrito não tem texto, só uma <span class="button-inner"> dentro, vou usar um seletor para botão que esteja visível e clicável
    print("Esperando botão pós-seleção de produto...")
    botao_pos_produto = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ion-button span.button-inner")))
    # Para clicar no botão pai ion-button
    driver.execute_script("arguments[0].parentElement.click();", botao_pos_produto)
    print("Botão após escolha do produto clicado.")

    # 9. Esperar página de formulário carregar
    wait.until(EC.url_contains("/gerentes/acompanhar-proposta/confirmar-dados"))
    print("Página do formulário carregada.")

    # 10. Preencher formulário (exemplo básico)
    preencher_ion_input("ion-input-48", "Ana Souza")  # Nome completo
    preencher_ion_input("ion-input-22", "123456")    # RG

    radio_feminino = wait.until(EC.element_to_be_clickable((By.XPATH, "//ion-radio[@value='F']")))
    driver.execute_script("arguments[0].click();", radio_feminino)

    preencher_ion_input("ion-input-23", "2000-01-01")
    preencher_ion_input("ion-input-25", "2000-01-01")
    preencher_ion_input("ion-input-24", "SSP")
    preencher_ion_input("ion-input-11", "72310008")
    preencher_ion_input("ion-input-28", "Maria Clara")
    preencher_ion_input("ion-input-30", "anadesouza@gmail.com")
    preencher_ion_input("ion-input-31", "61999989899")

    checkbox_sem_numero = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ion-checkbox[formcontrolname='noNumEndereco']")))
    driver.execute_script("arguments[0].click();", checkbox_sem_numero)
    print("Checkbox 'Sem número' clicado.")

    botao_proximo = wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//div[contains(@class, 'botao-proximo')]//ion-button[contains(., 'Próximo') and not(@disabled)]"
    )))
    botao_proximo.click()
    print("Botão 'Próximo' clicado.")

    time.sleep(5)

except Exception as e:
    print("Erro no script:", e)

finally:
    driver.quit()