import pygame
import sys
import random

class Submarino:
    def __init__(self, x, y):
        self.imagem_original = pygame.image.load("images/submarino.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem_original, (80, 80))
        self.rect = self.imagem.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = 5

    def mover(self):
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade

        if self.rect.x < 0: self.rect.x = 0
        if self.rect.x > 800 - 80: self.rect.x = 800 - 80
        if self.rect.y < 0: self.rect.y = 0
        if self.rect.y > 600 - 50: self.rect.y = 600 - 50

    def desenhar(self, janela):
        janela.blit(self.imagem, self.rect)


class Tubarao:
    def __init__(self):
        self.imagem_original = pygame.image.load("images/tubarao.png").convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem_original, (90, 90))
        self.rect = self.imagem.get_rect()
        self.rect.x = 850
        self.rect.y = random.randint(50,520)
        self.velocidade = random.randint(4, 7)
    
    def mover(self):
        self.rect.x -= self.velocidade
    
    def desenhar(self, janela):
        janela.blit(self.imagem, self.rect)


class Jogo:
    def __init__(self):
        pygame.init()
        self.LARGURA, self.ALTURA = 800, 600
        self.janela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Submarino vs Tubarões")
        self.relogio = pygame.time.Clock()

        self.estado = "MENU"

        self.fonte_minecraft_grande = pygame.font.Font("fontes/Minecraft.ttf", 45)
        self.fonte_minecraft_pqna = pygame.font.Font("fontes/Minecraft.ttf", 18)
        self.fonte_instrucoes = pygame.font.Font("fontes/Minecraft.ttf", 25)

        self.CINZA_BOTAO = (150, 150, 150)
        self.CINZA_BOTAO_HOVER = (180, 220, 180)
        self.TEXTO_SOMBRA = (60, 60, 60)
        self.BRANCO = (255, 255, 255)
        self.AMARELO_MINECRAFT = (255, 255, 0)
        self.AZUL_ESCURO = (10, 30, 60)
        self.AZUL_MAR = (20, 80, 150)
        self.BRANCO = (255, 255, 255)
        self.AMARELO = (255, 220, 0)
        self.VERMELHO = (200, 30, 30)
        self.VERDE = (30, 180, 30)

        self.fundo_menu = pygame.image.load("images/fundo_menu.png").convert()
        self.fundo_menu = pygame.transform.scale(self.fundo_menu, (self.LARGURA, self.ALTURA))

        self.imagem_fundo = pygame.image.load("images/fundo_mar.png").convert()
        self.imagem_fundo = pygame.transform.scale(self.imagem_fundo, (self.LARGURA, self.ALTURA))

        self.resetar_jogo()

    def resetar_jogo(self):
        self.jogador = Submarino(100, 300)
        self.tubaroes = []
        self.temporizador_inimigo = 0
        self.pontuacao = 0

        self.fundo_x1 = 0
        self.fundo_x2 = self.LARGURA
        self.velocidade_fundo = 2

    def gerir_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if self.estado == "MENU" and evento.key == pygame.K_SPACE:
                    self.resetar_jogo()
                    self.estado = "JOGANDO"
                elif (self.estado == "DERROTA" or self.estado == "VITORIA") and evento.key == pygame.K_SPACE:
                    self.estado = "MENU"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.estado == "MENU":
                    rect_botao = pygame.Rect(200, 400, 400, 50)
                    if rect_botao.collidepoint(evento.pos):
                        self.resetar_jogo()
                        self.estado = "JOGANDO"
                elif self.estado == "DERROTA":
                    rect_botao_recomecar = pygame.Rect(200, 400, 400, 50)
                    if rect_botao_recomecar.collidepoint(evento.pos):
                        self.estado = "MENU"
                elif self.estado == "VITORIA":
                    rect_botao_vitoria = pygame.Rect(200, 400, 400, 50)
                    if rect_botao_vitoria.collidepoint(evento.pos):
                        self.estado = "MENU"

    def desenhar_menu(self):
            self.janela.blit(self.fundo_menu, (0, 0))

            texto_titulo = "SUBMARINO VS TUBAROES"
            titulo_sombra = self.fonte_minecraft_grande.render(texto_titulo, True, self.TEXTO_SOMBRA)
            self.janela.blit(titulo_sombra, (64, 104))

            titulo_principal = self.fonte_minecraft_grande.render(texto_titulo, True, self.BRANCO)
            self.janela.blit(titulo_principal, (60, 100))

            txt_ctrl = self.fonte_minecraft_pqna.render("Controles: Use W, A, S, D ou as Setas para mover.", True, self.BRANCO)
            txt_obj = self.fonte_minecraft_pqna.render("Objetivo: Desvie dos tubaroes ate os 50 pontos!", True, self.BRANCO)

            self.janela.blit(txt_ctrl, (120, 220))
            self.janela.blit(txt_obj, (120, 260))

            rect_botao = pygame.Rect(200, 400, 400, 50)
            pos_mouse = pygame.mouse.get_pos()

            if rect_botao.collidepoint(pos_mouse):
                cor_atual_botao = self.CINZA_BOTAO_HOVER
                cor_texto_botao = self.AMARELO_MINECRAFT
            else:
                cor_atual_botao = self.CINZA_BOTAO
                cor_texto_botao = self.BRANCO

            pygame.draw.rect(self.janela, (0, 0, 0), rect_botao)
            pygame.draw.rect(self.janela, cor_atual_botao, rect_botao.inflate(-4, -4))

            txt_botao = self.fonte_minecraft_pqna.render("CLIQUE OU [ESPAÇO] PARA JOGAR", True, cor_texto_botao)
            texto_rect = txt_botao.get_rect(center=rect_botao.center)
            self.janela.blit(txt_botao, texto_rect)
            
    def desenhar_jogo(self):
        self.fundo_x1 -= self.velocidade_fundo
        self.fundo_x2 -= self.velocidade_fundo
        
        if self.fundo_x1 <= -self.LARGURA:
            self.fundo_x1 = self.LARGURA

        if self.fundo_x2 <= -self.LARGURA:
            self.fundo_x2 = self.LARGURA

        self.janela.blit(self.imagem_fundo, (self.fundo_x1, 0))
        self.janela.blit(self.imagem_fundo, (self.fundo_x2, 0))

        self.jogador.mover()
        self.jogador.desenhar(self.janela)

        self.temporizador_inimigo += 1
        if self.temporizador_inimigo >= 30:
            self.tubaroes.append(Tubarao())
            self.temporizador_inimigo = 0
            self.pontuacao += 1

        for tubarao in self.tubaroes[:]:
            tubarao.mover()
            tubarao.desenhar(self.janela)

            if tubarao.rect.x < -70:
                self.tubaroes.remove(tubarao)

            caixa_jogador = self.jogador.rect.inflate(-20, -20)
            caixa_tubarao = tubarao.rect.inflate(-50, -50)

            if caixa_jogador.colliderect(caixa_tubarao):
                self.estado = "DERROTA"

        texto_pontos = self.fonte_instrucoes.render(f"Pontos: {self.pontuacao} / 50", True, self.BRANCO)
        self.janela.blit(texto_pontos, (20, 20))

        if self.pontuacao >= 50:
            self.estado = "VITORIA"

    def desenhar_derrota(self):
        self.janela.fill((100, 10, 10))
        texto_morte = "GAME OVER!"

        centro_x = self.LARGURA // 2

        sombra_morte = self.fonte_minecraft_grande.render(texto_morte, True, (40, 0, 0))
        titulo_morte = self.fonte_minecraft_grande.render(texto_morte, True, (255, 50, 50))

        rect_sombra = sombra_morte.get_rect(center=(centro_x + 4, 154))
        rect_titulo = titulo_morte.get_rect(center=(centro_x, 150))
        self.janela.blit(sombra_morte, rect_sombra)
        self.janela.blit(titulo_morte, rect_titulo)

        texto_score = f"Pontos alcançados: {self.pontuacao}"
        txt_pontos_sombra = self.fonte_minecraft_pqna.render(texto_score, True, self.TEXTO_SOMBRA)
        txt_pontos_principal = self.fonte_minecraft_pqna.render(texto_score, True, self.BRANCO)

        rect_score_sombra = txt_pontos_sombra.get_rect(center=(centro_x + 2, 262))
        rect_score_principal = txt_pontos_principal.get_rect(center=(centro_x, 260))
        self.janela.blit(txt_pontos_sombra, rect_score_sombra)
        self.janela.blit(txt_pontos_principal, rect_score_principal)

        rect_botao_recomecar = pygame.Rect(200, 400, 400, 50)

        pos_mouse = pygame.mouse.get_pos()
        
        if rect_botao_recomecar.collidepoint(pos_mouse):
            cor_atual_botao = self.CINZA_BOTAO_HOVER
            cor_texto_botao = self.AMARELO_MINECRAFT
        else:
            cor_atual_botao = self.CINZA_BOTAO
            cor_texto_botao = self.BRANCO
 
        pygame.draw.rect(self.janela, (0, 0, 0), rect_botao_recomecar)
        pygame.draw.rect(self.janela, cor_atual_botao, rect_botao_recomecar.inflate(-4, -4))

        txt_botao = self.fonte_minecraft_pqna.render("CLIQUE OU [ESPAÇO] PARA O MENU", True, cor_texto_botao)
        texto_rect = txt_botao.get_rect(center=rect_botao_recomecar.center)
        self.janela.blit(txt_botao, texto_rect)

    def desenhar_vitoria(self):
        self.janela.fill((15, 90, 30))
        texto_ganhou = "VITÓRIA!"
        centro_x = self.LARGURA // 2

        sombra_vitoria = self.fonte_minecraft_grande.render(texto_ganhou, True, (5, 35, 10))
        titulo_vitoria = self.fonte_minecraft_grande.render(texto_ganhou, True, self.AMARELO_MINECRAFT)

        rect_sombra = sombra_vitoria.get_rect(center=(centro_x + 4, 154))
        rect_titulo = titulo_vitoria.get_rect(center=(centro_x, 150))

        texto_sub = "Você escapou dos tubarões!"
        txt_sub_sombra = self.fonte_minecraft_pqna.render(texto_sub, True, self.TEXTO_SOMBRA)
        txt_sub_principal = self.fonte_minecraft_pqna.render(texto_sub, True, self.BRANCO)

        rect_sub_sombra = txt_sub_sombra.get_rect(center=(centro_x + 2, 252))
        rect_sub_principal = txt_sub_principal.get_rect(center=(centro_x, 250))
        
        self.janela.blit(txt_sub_sombra, rect_sub_sombra)
        self.janela.blit(txt_sub_principal, rect_sub_principal)

        rect_botao_vitoria = pygame.Rect(200, 400, 400, 50)
        pos_mouse = pygame.mouse.get_pos()

        if rect_botao_vitoria.collidepoint(pos_mouse):
            cor_atual_botao = self.CINZA_BOTAO_HOVER
            cor_texto_botao = self.AMARELO_MINECRAFT
        else:
            cor_atual_botao = self.CINZA_BOTAO
            cor_texto_botao = self.BRANCO

        pygame.draw.rect(self.janela, (0, 0, 0), rect_botao_vitoria)
        pygame.draw.rect(self.janela, cor_atual_botao, rect_botao_vitoria.inflate(-4, -4))

        txt_botao = self.fonte_minecraft_pqna.render("CLIQUE OU [ESPAÇO] PARA O MENU", True, cor_texto_botao)
        texto_rect = txt_botao.get_rect(center=rect_botao_vitoria.center)
        self.janela.blit(txt_botao, texto_rect)
        
    def rodar(self):
        while True:
            self.gerir_eventos()

            if self.estado == "MENU":
                self.desenhar_menu()
            elif self.estado == "JOGANDO":
                self.desenhar_jogo()
            elif self.estado == "DERROTA":
                self.desenhar_derrota()
            elif self.estado == "VITORIA":
                self.desenhar_vitoria()

            pygame.display.flip()
            self.relogio.tick(60)

if __name__ == "__main__":
    meu_jogo = Jogo()
    meu_jogo.rodar()