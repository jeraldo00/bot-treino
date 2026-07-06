import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Tamanho da janela
LARGURA_TELA = 400
ALTURA_TELA = 600

# Cores
AZUL_CEU = (135, 206, 235)
VERDE = (0, 200, 0)
MARROM = (139, 69, 19)
BRANCO = (255, 255, 255)

# Configurações do jogo
GRAVIDADE = 0.5
FORCA_PULO = -8
VELOCIDADE_CANO = 4
DISTANCIA_CANO = 200

# Inicializa tela e fonte
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Flappy Bird - José Eraldo")
fonte = pygame.font.SysFont("Arial", 32)

# Carrega imagem do pássaro
passaro_img = pygame.image.load("passaro.png").convert_alpha()
passaro_img = pygame.transform.scale(passaro_img, (40, 40))  # redimensiona


# Função para desenhar o chão
def desenhar_chao():
    pygame.draw.rect(tela, MARROM, (0, ALTURA_TELA - 50, LARGURA_TELA, 50))

# Classe para o pássaro
class Passaro:
    def __init__(self):
        self.x = 50
        self.y = ALTURA_TELA // 2
        self.velocidade = 0
        self.img = passaro_img
        self.rect = self.img.get_rect(center=(self.x, self.y))

    def pular(self):
        self.velocidade = FORCA_PULO

    def mover(self):
        self.velocidade += GRAVIDADE
        self.y += self.velocidade
        self.rect.center = (self.x, self.y)

    def desenhar(self):
        tela.blit(self.img, self.rect)

# Classe para os canos
class Cano:
    def __init__(self, x):
        self.altura = random.randint(100, 400)
        self.x = x
        self.largura = 70

    def mover(self):
        self.x -= VELOCIDADE_CANO

    def desenhar(self):
        # Cano de cima
        pygame.draw.rect(tela, VERDE, (self.x, 0, self.largura, self.altura - DISTANCIA_CANO // 2))
        # Cano de baixo
        pygame.draw.rect(tela, VERDE, (self.x, self.altura + DISTANCIA_CANO // 2, self.largura, ALTURA_TELA))

    def fora_da_tela(self):
        return self.x + self.largura < 0

# Função principal
def main():
    relogio = pygame.time.Clock()
    passaro = Passaro()
    canos = [Cano(300)]
    pontuacao = 0
    rodando = True
    jogo_ativo = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and jogo_ativo:
                    passaro.pular()
                if evento.key == pygame.K_KP_ENTER and not jogo_ativo:
                    main()

        if jogo_ativo:
            # Movimento do pássaro
            passaro.mover()

            # Movimento dos canos
            for cano in canos:
                cano.mover()

            # Adiciona novo cano
            if canos[-1].x < 200:
                canos.append(Cano(LARGURA_TELA))

            # Remove canos fora da tela
            if canos[0].fora_da_tela():
                canos.pop(0)
                pontuacao += 1

            # Verifica colisões
            for cano in canos:
                if passaro.rect.colliderect(pygame.Rect(cano.x, 0, cano.largura, cano.altura - DISTANCIA_CANO // 2)) \
                   or passaro.rect.colliderect(pygame.Rect(cano.x, cano.altura + DISTANCIA_CANO // 2, cano.largura, ALTURA_TELA)):
                    jogo_ativo = False

            # Se tocar o chão ou sair da tela
            if passaro.y >= ALTURA_TELA - 50 or passaro.y < 0:
                jogo_ativo = False

        # Desenha tudo
        tela.fill(AZUL_CEU)
        for cano in canos:
            cano.desenhar()
        desenhar_chao()
        passaro.desenhar()

        # Pontuação
        texto = fonte.render(f"Pontos: {pontuacao}", True, BRANCO)
        tela.blit(texto, (10, 10))

        # Tela de game over
        if not jogo_ativo:
            fim_texto = fonte.render("GAME OVER", True, (255, 0, 0))
            reiniciar = pygame.font.SysFont("Arial", 24).render("Pressione ENTER para reiniciar", True, BRANCO)
            tela.blit(fim_texto, (LARGURA_TELA//2 - fim_texto.get_width()//2, ALTURA_TELA//2 - 40))
            tela.blit(reiniciar, (LARGURA_TELA//2 - reiniciar.get_width()//2, ALTURA_TELA//2 + 10))

        pygame.display.update()
        relogio.tick(60)

if __name__ == "__main__":
    main()
