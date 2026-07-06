from selenium.webdriver.common.by import By

CAMPO_USUARIO = (By.NAME, "username")
CAMPO_SENHA = (By.NAME, "password")
BOTAO_ACESSAR = (By.XPATH, "//button[contains(text(), 'Iniciar sessão')]")
MENU_PESQUISA = (By.LINK_TEXT, "PESQUISA")
SUBMENU_PLANOS_TESTE = (By.XPATH, '//*[@id="navbar"]/div[2]/ul[2]/li[3]/ul/li[1]/a')
