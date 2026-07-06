from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver import get_driver
import time

URL = "https://piepe-tst.brbcard.com.br/"

USUARIO = "02531540148"   # somente números
SENHA = "Brbcard@1"

def login_piepe():
    driver = get_driver()
    wait = WebDriverWait(driver, 20)

    driver.get(URL)

    try:
        # Aguarda campo CPF
        campo_cpf = wait.until(
            EC.visibility_of_element_located((By.ID, "cpf"))
        )
        campo_senha = wait.until(
            EC.visibility_of_element_located((By.ID, "senha"))
        )

        campo_cpf.clear()
        campo_cpf.send_keys(USUARIO)

        campo_senha.clear()
        campo_senha.send_keys(SENHA)

        # Botão Entrar (ajuste se necessário)
        botao_entrar = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        botao_entrar.click()

        # Aguarda carregamento da tela inicial após login
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print("✅ Login realizado com sucesso no PIEPE!")

    except Exception as e:
        print("❌ Erro ao realizar login:", e)

    time.sleep(5)
    driver.quit()

if __name__ == "__main__":
    login_piepe()
