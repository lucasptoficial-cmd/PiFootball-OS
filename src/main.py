#!/usr/bin/env python3
"""Protótipo leve da interface PiFootball OS."""
import sys
from datetime import datetime
try:
    import pygame
except ImportError:
    print('Pygame em falta. Instala com: sudo apt install python3-pygame')
    raise SystemExit(1)

W, H = 1280, 720
BG=(12,14,18); PANEL=(24,27,33); ORANGE=(255,119,32); WHITE=(242,244,247); MUTED=(153,160,170)
ITEMS=[('FUTEBOL','Jogos, resultados e competições'),('TV','Canais e guia de programação'),('INTERNET','Navegador e serviços online'),('FILMES E SÉRIES','Biblioteca multimédia'),('APLICAÇÕES','As tuas aplicações'),('MÚSICA','Música e rádio'),('NOTÍCIAS','Notícias desportivas'),('DEFINIÇÕES','Perfis, rede e sistema'),('IPTV','Ligar a um servidor IPTV')]

def main():
    pygame.init(); pygame.display.set_caption('PiFootball OS')
    screen=pygame.display.set_mode((W,H),pygame.RESIZABLE); clock=pygame.time.Clock()
    big=pygame.font.Font(None,58); med=pygame.font.Font(None,28); small=pygame.font.Font(None,21)
    selected=0; message='Bem-vindo ao PiFootball OS'; running=True
    while running:
        w,h=screen.get_size()
        for e in pygame.event.get():
            if e.type==pygame.QUIT: running=False
            elif e.type==pygame.KEYDOWN:
                if e.key in (pygame.K_ESCAPE,pygame.K_q): running=False
                elif e.key in (pygame.K_RIGHT,pygame.K_DOWN): selected=(selected+1)%len(ITEMS)
                elif e.key in (pygame.K_LEFT,pygame.K_UP): selected=(selected-1)%len(ITEMS)
                elif e.key in (pygame.K_RETURN,pygame.K_KP_ENTER): message=ITEMS[selected][0]+' — módulo ainda em desenvolvimento'
        screen.fill(BG); pygame.draw.rect(screen,PANEL,(0,0,w,108))
        screen.blit(big.render('PiFOOTBALL',True,WHITE),(38,24)); screen.blit(big.render('OS',True,ORANGE),(345,24))
        stamp=small.render(datetime.now().strftime('%d/%m/%Y   %H:%M'),True,MUTED); screen.blit(stamp,(w-stamp.get_width()-30,45))
        screen.blit(big.render('O TEU CENTRO DE ENTRETENIMENTO',True,WHITE),(40,140))
        cols=3; gap=14; cardw=(w-80-(cols-1)*gap)//cols; cardh=112
        for i,(name,desc) in enumerate(ITEMS):
            row,col=divmod(i,cols); x=40+col*(cardw+gap); y=225+row*(cardh+14)
            rect=pygame.Rect(x,y,cardw,cardh); pygame.draw.rect(screen,PANEL,rect,border_radius=10)
            if i==selected: pygame.draw.rect(screen,ORANGE,rect,width=4,border_radius=10)
            screen.blit(med.render(name,True,ORANGE if i==selected else WHITE),(x+14,y+20))
            screen.blit(small.render(desc,True,MUTED),(x+14,y+62))
        pygame.draw.rect(screen,PANEL,(0,h-48,w,48)); screen.blit(small.render(message,True,WHITE),(20,h-31))
        hint=small.render('Setas: navegar   ENTER: abrir   ESC: sair',True,MUTED); screen.blit(hint,(w-hint.get_width()-20,h-31))
        pygame.display.flip(); clock.tick(30)
    pygame.quit(); return 0
if __name__=='__main__': raise SystemExit(main())
