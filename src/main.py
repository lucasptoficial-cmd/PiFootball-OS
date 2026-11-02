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
PROFILES_FILE = CONFIG_DIR / "profiles.json"
SETTINGS_FILE = CONFIG_DIR / "settings.json"

ITEMS = [
    ("FUTEBOL", "Jogos, resultados e competições"),
    ("TV & IPTV", "Canais, guia e listas IPTV"),
    ("INTERNET", "Navegador e serviços online"),
    ("FILMES E SÉRIES", "Biblioteca multimédia"),
    ("APLICAÇÕES", "As tuas aplicações"),
    ("MÚSICA", "Música e rádio"),
    ("NOTÍCIAS", "Notícias desportivas"),
    ("DEFINIÇÕES", "Perfis, rede e sistema"),
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

def load_profiles():
    try:
        data = json.loads(PROFILES_FILE.read_text(encoding="utf-8"))
        names = data.get("profiles", [])
        active = data.get("active", "")
        names = [str(n).strip() for n in names if str(n).strip()]
        if names:
            return names, active if active in names else names[0]
    except (OSError, ValueError, TypeError):
        pass
    return ["Utilizador"], "Utilizador"

def save_profiles(names, active):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = {"profiles": names, "active": active}
    PROFILES_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(PROFILES_FILE, 0o600)
    except OSError:
        pass

def load_settings():
    defaults = {"boot_animation": True}
    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        defaults.update({k: data[k] for k in defaults if k in data})
    except (OSError, ValueError, TypeError):
        pass
    return defaults

def save_settings(settings):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(SETTINGS_FILE, 0o600)
    except OSError:
        pass

def draw_boot_animation(screen, clock):
    """Animação de arranque integrada no sistema, antes do HOME."""
    width, height = screen.get_size()
    title_font = pygame.font.Font(None, 104)
    subtitle_font = pygame.font.Font(None, 30)
    status_font = pygame.font.Font(None, 25)
    started = pygame.time.get_ticks()
    duration = 6800
    services = ["A iniciar interface", "A verificar serviços", "A preparar o ambiente"]

    while True:
        now = pygame.time.get_ticks()
        elapsed = now - started
        progress = min(1.0, elapsed / duration)
        phase = elapsed / duration
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        screen.fill((3, 5, 8))
        cx, cy = width // 2, height // 2 - 35

        # Reflexo verde que atravessa o ecrã no início.
        if phase < 0.43:
            sweep = (phase / 0.43) * (width + 500) - 250
            glow = pygame.Surface((width, height), pygame.SRCALPHA)
            for offset in range(-150, 151, 5):
                alpha = max(0, 34 - abs(offset) // 5)
                pygame.draw.line(glow, (25, 220, 125, alpha),
                                 (int(sweep + offset), 0),
                                 (int(sweep + offset - 210), height), 2)
            screen.blit(glow, (0, 0))
            pulse = 0.5 + 0.5 * __import__("math").sin(elapsed / 260)
            pygame.draw.circle(screen, (12, int(65 + 55 * pulse), 55),
                               (width // 2, cy), int(100 + 25 * pulse), 2)

        # Marca central e feixe de luz.
        logo_color = (235, 245, 240) if phase < 0.58 else (255, 255, 255)
        logo = title_font.render("PiFOOTBALL", True, logo_color)
        os_mark = title_font.render("OS", True, (255, 126, 35))
        total_w = logo.get_width() + os_mark.get_width() + 12
        x = (width - total_w) // 2
        logo_rect = logo.get_rect(topleft=(x, cy - 55))
        screen.blit(logo, logo_rect)
        screen.blit(os_mark, (x + logo.get_width() + 12, cy - 55))

        if 0.18 < phase < 0.66:
            sweep_p = (phase - 0.18) / 0.48
            beam_x = x - 80 + int(sweep_p * (total_w + 160))
            beam = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.line(beam, (255, 255, 255, 150),
                             (beam_x, cy - 75), (beam_x - 90, cy + 30), 5)
            pygame.draw.line(beam, (80, 255, 170, 70),
                             (beam_x + 8, cy - 75), (beam_x - 82, cy + 30), 15)
            screen.blit(beam, (0, 0))

        sub = subtitle_font.render("O TEU CENTRO DE ENTRETENIMENTO", True, (155, 165, 170))
        screen.blit(sub, sub.get_rect(center=(width // 2, cy + 65)))

        if phase >= 0.55:
            idx = min(len(services) - 1, int((phase - 0.55) / 0.45 * len(services)))
            status = status_font.render(services[idx] + "...", True,
                                        (255, 145, 65) if phase > 0.78 else (85, 210, 145))
            screen.blit(status, status.get_rect(center=(width // 2, cy + 135)))
            bar_w = min(420, width - 80)
            bar = pygame.Rect((width - bar_w) // 2, cy + 170, bar_w, 8)
            pygame.draw.rect(screen, (35, 42, 45), bar, border_radius=4)
            fill = bar.copy()
            fill.width = int(bar_w * max(0, min(1, (phase - 0.55) / 0.45)))
            if fill.width:
                pygame.draw.rect(screen, (255, 126, 35), fill, border_radius=4)

        # A luz verde transforma-se gradualmente no brilho laranja do HOME.
        if phase > 0.82:
            fade = min(1.0, (phase - 0.82) / 0.18)
            tint = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.rect(tint, (255, 105, 25, int(34 * fade)), (0, 0, width, height))
            screen.blit(tint, (0, 0))

        pygame.display.flip()
        if elapsed >= duration:
            return True
        clock.tick(30)


def draw_goal_placeholder(screen, elapsed_ms):
    """Alerta temporário de golo desenhado pelo Pygame; será substituído pelo GIF do utilizador."""
    width, height = screen.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    pulse = 0.5 + 0.5 * __import__("math").sin(elapsed_ms / 110)
    overlay.fill((0, 0, 0, int(175 + 45 * pulse)))
    screen.blit(overlay, (0, 0))
    center = (width // 2, height // 2)
    radius = int(95 + 14 * pulse)
    pygame.draw.circle(screen, (255, 126, 35), center, radius, 7)
    pygame.draw.circle(screen, (255, 205, 95), center, radius + 15, 2)
    title_font = pygame.font.Font(None, 112)
    info_font = pygame.font.Font(None, 38)
    small_font = pygame.font.Font(None, 24)
    for text_value, font_obj, color, offset in [
        ("GOLO!", title_font, (255,255,255), -25),
        ("A TUA EQUIPA", info_font, (255,145,55), 55),
        ("1  -  0", info_font, (255,255,255), 100),
        ("DEMO  •  ALERTA TEMPORÁRIO", small_font, (190,198,205), 155),
    ]:
        surf = font_obj.render(text_value, True, color)
        screen.blit(surf, surf.get_rect(center=(center[0], center[1] + offset)))


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
    settings_index = 0
    profiles, active_profile = load_profiles()
    new_profile_name = ""
    settings = load_settings()
    config = load_iptv()
    password = ""
    message = "Bem-vindo ao PiFootball OS"
    goal_alert_started = None
    running = draw_boot_animation(screen, clock) if settings["boot_animation"] else True

    while running:
        width, height = screen.get_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if page == "home":
                    if event.key in (pygame.K_ESCAPE, pygame.K_q):
                        running = False
                    elif event.key == pygame.K_F9:
                        goal_alert_started = pygame.time.get_ticks()
                        message = "Demonstração de alerta de golo"
                    elif event.key in (pygame.K_RIGHT, pygame.K_DOWN):
                        selected = (selected + 1) % len(ITEMS)
                    elif event.key in (pygame.K_LEFT, pygame.K_UP):
                        selected = (selected - 1) % len(ITEMS)
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if ITEMS[selected][0] == "TV & IPTV":
                            page = "iptv"
                            field_index = 0
                        elif ITEMS[selected][0] == "DEFINIÇÕES":
                            page = "settings"
                            settings_index = 0
                        else:
                            message = ITEMS[selected][0] + " — módulo em desenvolvimento"
                elif page == "settings":
                    if event.key == pygame.K_ESCAPE:
                        page = "home"
                    elif event.key in (pygame.K_UP, pygame.K_DOWN):
                        settings_index = (settings_index + (1 if event.key == pygame.K_DOWN else -1)) % 2
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if settings_index == 0:
                            settings["boot_animation"] = not settings["boot_animation"]
                            save_settings(settings)
                            message = "Animação de arranque " + ("ativada" if settings["boot_animation"] else "desativada")
                        else:
                            page = "users"
                elif page == "settings":
            screen.blit(big.render("DEFINIÇÕES", True, WHITE), (42, 145))
            screen.blit(small.render("Configuração geral do PiFootball OS", True, MUTED), (46, 205))
            options = [("Animação de arranque", "ATIVADA" if settings["boot_animation"] else "DESATIVADA"), ("Gerir utilizadores", "ABRIR")]
            for i, (label, value) in enumerate(options):
                y = 270 + i * 100
                rect = pygame.Rect(44, y, min(width - 88, 900), 76)
                pygame.draw.rect(screen, PANEL, rect, border_radius=9)
                if i == settings_index:
                    pygame.draw.rect(screen, ORANGE, rect, width=3, border_radius=9)
                screen.blit(med.render(label, True, WHITE), (rect.x + 18, rect.y + 20))
                val = small.render(value, True, GREEN if i == 0 else ORANGE)
                screen.blit(val, (rect.right - val.get_width() - 20, rect.y + 27))
            screen.blit(small.render("CIMA/BAIXO: escolher   ENTER: alterar/abrir   ESC: voltar", True, MUTED), (44, height - 55))
        elif page == "users":
                    if event.key == pygame.K_ESCAPE:
                        page = "home"
                    elif event.key in (pygame.K_UP, pygame.K_DOWN):
                        if profiles:
                            current = profiles.index(active_profile) if active_profile in profiles else 0
                            step = -1 if event.key == pygame.K_UP else 1
                            active_profile = profiles[(current + step) % len(profiles)]
                            save_profiles(profiles, active_profile)
                            message = "Utilizador ativo: " + active_profile
                    elif event.key == pygame.K_F2:
                        if len(profiles) > 1:
                            profiles.remove(active_profile)
                            active_profile = profiles[0]
                            save_profiles(profiles, active_profile)
                            message = "Perfil removido. Ativo: " + active_profile
                        else:
                            message = "Mantém pelo menos um perfil."
                    elif event.key == pygame.K_F5:
                        settings["boot_animation"] = not settings["boot_animation"]
                        save_settings(settings)
                        message = "Animação de arranque " + ("ativada" if settings["boot_animation"] else "desativada")
                    elif event.key == pygame.K_BACKSPACE:
                        new_profile_name = new_profile_name[:-1]
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        candidate = new_profile_name.strip()
                        if candidate:
                            existing = next((n for n in profiles if n.casefold() == candidate.casefold()), None)
                            if existing:
                                active_profile = existing
                            else:
                                profiles.append(candidate)
                                active_profile = candidate
                            save_profiles(profiles, active_profile)
                            message = "Utilizador ativo: " + active_profile
                            new_profile_name = ""
                        else:
                            message = "Escreve um nome primeiro."
                    elif event.unicode and event.unicode.isprintable() and len(new_profile_name) < 24:
                        new_profile_name += event.unicode
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
            screen.blit(small.render("Perfil: " + active_profile, True, GREEN), (42, 190))
            cols, gap, cardh = 4, 14, 150
            cardw = (width - 80 - (cols - 1) * gap) // cols
            for i, (name, desc) in enumerate(ITEMS):
                row, col = divmod(i, cols)
                x, y = 40 + col * (cardw + gap), 250 + row * (cardh + 18)
                rect = pygame.Rect(x, y, cardw, cardh)
                pygame.draw.rect(screen, PANEL, rect, border_radius=10)
                if i == selected:
                    pygame.draw.rect(screen, ORANGE, rect, width=4, border_radius=10)
                screen.blit(med.render(name, True, ORANGE if i == selected else WHITE), (x + 18, y + 28))
                screen.blit(small.render(desc, True, MUTED), (x + 18, y + 78))
        elif page == "users":
            screen.blit(big.render("UTILIZADORES", True, WHITE), (42, 145))
            screen.blit(small.render("Perfil ativo: " + active_profile, True, GREEN), (46, 210))
            screen.blit(med.render("Perfis guardados", True, WHITE), (46, 260))
            for i, name in enumerate(profiles[:10]):
                color = ORANGE if name == active_profile else MUTED
                screen.blit(med.render(name, True, color), (60, 305 + i * 36))
            box = pygame.Rect(620, 260, min(560, width - 660), 72)
            pygame.draw.rect(screen, PANEL, box, border_radius=8)
            pygame.draw.rect(screen, ORANGE, box, 2, border_radius=8)
            screen.blit(small.render("Criar ou selecionar perfil", True, MUTED), (box.x + 14, box.y + 8))
            screen.blit(med.render(new_profile_name or "Escreve um nome...", True, WHITE), (box.x + 14, box.y + 36))
            screen.blit(small.render("Cima/baixo: trocar perfil   ENTER: criar/selecionar   F2: apagar perfil", True, MUTED), (44, height - 92))
            screen.blit(small.render("F5: animação de arranque " + ("ATIVADA" if settings["boot_animation"] else "DESATIVADA") + "   ESC: voltar", True, MUTED), (44, height - 62))
            screen.blit(small.render("Os perfis são guardados localmente neste Raspberry Pi.", True, GREEN), (44, height - 34))
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

        if goal_alert_started is not None:
            goal_elapsed = pygame.time.get_ticks() - goal_alert_started
            if goal_elapsed < 4500:
                draw_goal_placeholder(screen, goal_elapsed)
            else:
                goal_alert_started = None

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
