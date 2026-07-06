import rpa as r
import pyautogui as p


r.init()
r.url('https://www.goal.com/br/listas/futebol-programacao-jogos-tv-aberta-fechada-onde-assistir-online-app/bltc0a7361374657315#csf40ac538563ee54a')
p.sleep(3)
p.getActiveWindow()
janela = p.getActiveWindow()
janela.maximize()