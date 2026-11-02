#!/usr/bin/env python3
"""PiFootball OS: interface inicial com formulário local de configuração IPTV.

A ligação e reprodução IPTV ainda não estão implementadas nesta versão.
As credenciais secretas não são gravadas em disco.
"""
import json
import os
from pathlib import Path
from datetime import datetime
import pygame

W, H = 1280, 720
BG=(12,14,18); PANEL=(24,27,33); ORANGE=(255,119,32)
WHITE=(242,244,247); MUTED=(153,160,170); GREEN=(75,190,125)
CONFIG_DIR = Path.home() / ".config" / "pifootball"
IPTV_FILE = CONFIG_DIR / "iptv.json"

ITEMS = [
    ("FUTEBOL", "Jogos, resultados e competições"),
    ("TV", "Canais e guia de programação"),
    ("INTERNET", "Navegador e serviços online"),
    ("FILMES E SÉRIES", "Biblioteca multimédia"),
    ("APLICAÇÕES", "As tuas aplicações"),
    ("MÚSICA", "Música e rádio"),
    ("NOTÍCIAS", "Notícias desportivas"),
    ("DEFINIÇÕES", "Perfis, rede e sistema"),
    ("IPTV", "Configurar host e lista de canais"),
]
FIELDS = [
    ("Host / IP", "host"),
    ("Porta", "port"),
    ("Utilizador", "username"),
    ("Palavra-passe", "password"),
    ("URL M3U (opcional)", "m3u"),
]

def load_iptv():
    try:
        data = json.loads(IPTV_FILE.read_text(encoding="utf-8"))
        return {k: str(data.get(k, "")) for k in ("host", "port", "username", "m3u")}
    except (OSError, ValueError, TypeError):
        return {"host": "", "port": "8080", "username": "", "m3u": ""}

def save_iptv(data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    safe = {k: data.get(k, "") for k in ("host", "port", "username", "m3u")}
    IPTV_FILE.write_text(json.dumps(safe, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(IPTV_FILE, 0o600)
    except OSError:
        pass

def main():
    pygame.init()
    pygame.display.set_caption("PiFootball OS")
    screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    big = pygame.font.Font(None, 58)
    med = pygame.font.Font(None, 30)
    small = pygame.font.Font(None, 22)
    selected = 0
    page = "home"
    field_index = 0
    config = load_iptv()
    password = ""
    message = "Bem-vindo ao PiFootball OS"
    running = True

    while running:
        width, height = screen.get_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if page == "home":
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                    elif event.key in (pygame.K_RIGHT, pygame.K_DOWN):
                        selected = (selected + 1) % len(ITEMS)
                    elif event.key in (pygame.K_LEFT, pygame.K_UP):
                        selected = (selected - 1) % len(ITEMS)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if ITEMS[selected][0] == "IPTV":
                            page = "iptv"
                            field_index = 0
                        else:
                            message = ITEMS[selected][0] + " — módulo em desenvolvimento"
                elif page == "iptv":
                    if event.key == pygame.K_ESCAPE:
                        page = "home"
                    elif event.key in (pygame.K_UP, pygame.K_DOWN):
                        field_index = (field_index + (-1 if event.key == pygame.K_UP else 1)) % len(FIELDS)
                    elif event.key == pygame.K_TAB:
                        field_index = (field_index + 1) % len(FIELDS)
                    elif event.key == pygame.K_BACKSPACE:
                        key = FIELDS[field_index][1]
                        if key == "password":
                            password = password[:-1]
                        else:
                            config[key] = config.get(key, "")[:-1]
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if field_index == len(FIELDS) - 1:
                            if not config["host"] and not config["m3u"]:
                                message = "Indica um host ou URL M3U antes de guardar."
                            else:
                                save_iptv(config)
                                message = "Configuração guardada. A reprodução ainda não está disponível."
                        else:
                            field_index = (field_index + 1) % len(FIELDS)
                    elif event.unicode and event.unicode.isprintable():
                        key = FIELDS[field_index][1]
                        if key == "password":
                            password += event.unicode
                        else:
                            config[key] = config.get(key, "") + event.unicode

        screen.fill(BG)
        pygame.draw.rect(screen, PANEL, (0, 0, width, 108))
        screen.blit(big.render("PiFOOTBALL", True, WHITE), (38, 24))
        screen.blit(big.render("OS", True, ORANGE), (345, 24))
        stamp = small.render(datetime.now().strftime("%d/%m/%Y   %H:%M"), True, MUTED)
        screen.blit(stamp, (width - stamp.get_width() - 30, 45))

        if page == "home":
            screen.blit(big.render("O TEU CENTRO DE ENTRETENIMENTO", True, WHITE), (40, 140))
            cols, gap, cardh = 3, 14, 112
            cardw = (width - 80 - (cols - 1) * gap) // cols
            for i, (name, desc) in enumerate(ITEMS):
                row, col = divmod(i, cols)
                x, y = 40 + col * (cardw + gap), 225 + row * (cardh + 14)
                rect = pygame.Rect(x, y, cardw, cardh)
                pygame.draw.rect(screen, PANEL, rect, border_radius=10)
                if i == selected:
                    pygame.draw.rect(screen, ORANGE, rect, width=4, border_radius=10)
                screen.blit(med.render(name, True, ORANGE if i == selected else WHITE), (x + 14, y + 20))
                screen.blit(small.render(desc, True, MUTED), (x + 14, y + 62))
        else:
            screen.blit(big.render("CONFIGURAR IPTV", True, WHITE), (42, 145))
            screen.blit(small.render("Introduz os dados fornecidos pelo teu serviço IPTV autorizado.", True, MUTED), (44, 205))
            for i, (label, key) in enumerate(FIELDS):
                y = 250 + i * 72
                active = i == field_index
                rect = pygame.Rect(44, y, min(width - 88, 900), 58)
                pygame.draw.rect(screen, PANEL, rect, border_radius=8)
                if active:
                    pygame.draw.rect(screen, ORANGE, rect, width=3, border_radius=8)
                screen.blit(small.render(label, True, MUTED), (rect.x + 14, rect.y + 7))
                value = password if key == "password" else config.get(key, "")
                shown = ("•" * len(value)) if key == "password" else value
                if not shown:
                    shown = "Escrever..."
                screen.blit(med.render(shown[:75], True, WHITE), (rect.x + 260, rect.y + 17))
            screen.blit(small.render("ENTER no último campo: guardar configuração   TAB/setas: mudar campo   ESC: voltar", True, MUTED), (44, height - 92))
            screen.blit(small.render("A palavra-passe fica apenas na memória desta sessão e não é guardada.", True, GREEN), (44, height - 62))
            screen.blit(small.render("Nota: esta versão guarda os dados básicos; ainda não liga nem reproduz canais.", True, MUTED), (44, height - 34))

        pygame.draw.rect(screen, PANEL, (0, height - 48, width, 48))
        screen.blit(small.render(message, True, WHITE), (20, height - 31))
        if page == "home":
            hint = small.render("Setas: navegar   ENTER: abrir   ESC: sair", True, MUTED)
            screen.blit(hint, (width - hint.get_width() - 20, height - 31))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
