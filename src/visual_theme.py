"""PiFootball OS neon-orange TV interface.
The layout is authored on a 1672x941 design canvas and scaled to the display.
"""
import math
import pygame
from datetime import datetime

BASE_W, BASE_H = 1672, 941
ORANGE = (255, 145, 0)
GOLD = (255, 190, 25)
WHITE = (248, 248, 248)
MUTED = (190, 194, 200)
DARK = (8, 8, 9)

NAV = [
    ("Futebol", "⚽"), ("TV", "▣"), ("Internet /\nNavegador", "◎"),
    ("Definições", "⚙"), ("Filmes e\nséries", "▣"),
    ("Aplicações", "▦"), ("Música", "♫"), ("Notícias\ndesportivas", "▤")
]

def _font(size, bold=False):
    return pygame.font.SysFont("DejaVu Sans", size, bold=bold)

def _text(dst, value, x, y, size, color=WHITE, bold=False, center=False):
    f = _font(size, bold)
    lines = str(value).split("\n")
    yy = y
    for line in lines:
        surf = f.render(line, True, color)
        rect = surf.get_rect()
        if center:
            rect.midtop = (x, yy)
        else:
            rect.topleft = (x, yy)
        dst.blit(surf, rect)
        yy += size + 3
    return yy

def _rounded(dst, rect, fill=(10, 9, 8), border=ORANGE, radius=24, width=3, glow=False):
    r = pygame.Rect(rect)
    if glow:
        for grow, alpha in ((14, 22), (8, 35), (4, 55)):
            layer = pygame.Surface((BASE_W, BASE_H), pygame.SRCALPHA)
            pygame.draw.rect(layer, (*border, alpha), r.inflate(grow, grow), border_radius=radius + grow//2)
            dst.blit(layer, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    pygame.draw.rect(dst, fill, r, border_radius=radius)
    if border:
        pygame.draw.rect(dst, border, r, width, border_radius=radius)

def _background(dst):
    dst.fill((4, 7, 12))
    # Stadium roof and night sky.
    for y in range(0, 460):
        t = y / 460
        c = (int(4 + 8*t), int(8 + 9*t), int(15 + 12*t))
        pygame.draw.line(dst, c, (0, y), (BASE_W, y))
    # Stadium floodlights on both sides.
    for cx, cy, direction in ((105, 75, 1), (1560, 70, -1)):
        for rad, alpha in ((150, 12), (100, 18), (55, 25)):
            glow = pygame.Surface((BASE_W, BASE_H), pygame.SRCALPHA)
            pygame.draw.circle(glow, (190, 215, 255, alpha), (cx, cy), rad)
            dst.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        for row in range(4):
            for col in range(7):
                x = cx + (col-3)*16
                y = cy + (row-1)*13
                pygame.draw.circle(dst, (220, 235, 255), (x, y), 4)
    # Stadium tiers and crowd lights.
    for y, color in ((180, (55, 46, 34)), (205, (80, 55, 27)), (232, (95, 60, 24)), (260, (34, 38, 31))):
        pygame.draw.line(dst, color, (0, y), (BASE_W, y), 3)
    for i in range(360):
        x = (i * 47) % BASE_W
        y = 270 + ((i * 31) % 120)
        c = (255, 145 + (i % 70), 35) if i % 3 else (230, 235, 240)
        pygame.draw.circle(dst, c, (x, y), 1 + (i % 2))
    # Pitch, touchlines and mowing stripes.
    pygame.draw.rect(dst, (15, 52, 20), (0, 385, BASE_W, 556))
    for i in range(9):
        x = i * 210
        pygame.draw.rect(dst, (17, 61, 23) if i % 2 else (20, 70, 26), (x, 385, 210, 556))
    pygame.draw.line(dst, (150, 175, 120), (0, 415), (BASE_W, 415), 3)
    pygame.draw.line(dst, (150, 175, 120), (0, 815), (BASE_W, 815), 2)
    # Subtle orange light streaks.
    for i in range(5):
        x = 1180 + i*90
        pygame.draw.line(dst, (115, 55, 10), (x, 0), (x-250, 440), 3)

def _ball(dst, cx, cy, radius):
    pygame.draw.circle(dst, (245, 245, 242), (cx, cy), radius)
    pygame.draw.circle(dst, (22, 22, 24), (cx, cy), radius, 5)
    pygame.draw.polygon(dst, (25, 25, 27), [(cx,cy-radius//3),(cx+radius//3,cy-radius//8),(cx+radius//4,cy+radius//3),(cx-radius//4,cy+radius//3),(cx-radius//3,cy-radius//8)])
    for dx,dy in ((-1,-1),(1,-1),(-1,1),(1,1)):
        pygame.draw.line(dst, (30,30,32), (cx,cy), (cx+dx*radius*3//4,cy+dy*radius*3//4), 4)
    pygame.draw.circle(dst, (255,255,255), (cx-radius//3,cy-radius//2), max(3,radius//8))

def _header(dst, selected):
    _text(dst, "▣", 88, 82, 86, WHITE, True)
    _text(dst, "PiFootball", 220, 78, 78, WHITE, True)
    _text(dst, "OS", 608, 78, 82, ORANGE, True)
    _text(dst, "O  T E U  M U N D O  D O  F U T E B O L", 265, 171, 20, WHITE, True)
    pygame.draw.line(dst, ORANGE, (210, 184), (250,184), 4)
    pygame.draw.line(dst, ORANGE, (730, 184), (790,184), 4)
    # Football and orbit mark.
    _ball(dst, 1030, 132, 108)
    orbit = pygame.Rect(830, 60, 400, 135)
    pygame.draw.ellipse(dst, (255, 130, 0), orbit, 9)
    pygame.draw.ellipse(dst, (255, 205, 45), orbit.inflate(-12,-12), 2)
    # Raspberry mark, simplified but recognizable.
    for dx,dy in ((0,0),(-22,18),(22,18),(-34,48),(0,52),(34,48),(-18,82),(18,82)):
        pygame.draw.circle(dst, (220, 0, 65), (1250+dx, 116+dy), 17)
    pygame.draw.ellipse(dst, (75, 210, 20), (1212, 90, 35, 18))
    pygame.draw.ellipse(dst, (75, 210, 20), (1250, 85, 35, 18))
    # Status capsule.
    _rounded(dst, (1290, 32, 335, 52), (10, 11, 13), (60, 60, 60), 24, 1)
    now = datetime.now()
    status = "◉   🎮  |  " + now.strftime("%H:%M") + "  |  " + now.strftime("%d/%m/%Y")
    _text(dst, status, 1310, 43, 19, WHITE, True)

def _nav(dst, selected):
    x0, y, w, h, gap = 52, 245, 195, 168, 13
    for i, (label, symbol) in enumerate(NAV):
        x = x0 + i*(w+gap)
        active = i == selected
        _rounded(dst, (x,y,w,h), (25,15,6) if active else (10,9,8),
                 (255,177,0) if active else (190,91,0), 23, 4 if active else 2, active)
        _text(dst, symbol, x+w//2, y+16, 58, WHITE, True, True)
        _text(dst, label, x+w//2, y+112 if "\n" not in label else y+100, 23, WHITE, True, True)

def _footer(dst, message=""):
    _rounded(dst, (0, 815, BASE_W, 110), (5,5,6), ORANGE, 22, 3)
    parts = [
        ("◉", "Navegar"), ("OK", "Selecionar"), ("↶", "Voltar"),
        ("⌂", "Menu Principal"), ("CH+ / CH−", "Mudar de canal"),
        ("i", "Segura OK ou carrega OK 5 vezes\npara voltar ao menu principal."),
        ("🎮", "Comando de jogo\napenas para jogos.")
    ]
    x = 30
    widths = [195,165,135,205,320,365,240]
    for i, (icon, label) in enumerate(parts):
        if i in (4,5,6):
            pygame.draw.line(dst, ORANGE, (x, 835), (x, 905), 4)
            x += 22
        _text(dst, icon, x, 842, 31 if len(icon)>2 else 38, ORANGE if icon=="i" else WHITE, True)
        _text(dst, label, x+48, 848, 17, WHITE, False)
        x += widths[i]
    if message:
        _text(dst, message, 835, 785, 16, GOLD, True)

def _panel(dst, rect, title, icon="▦"):
    _rounded(dst, rect, (10,8,6), (230,112,0), 26, 3)
    _text(dst, icon, rect[0]+38, rect[1]+18, 42, GOLD, True)
    _text(dst, title, rect[0]+108, rect[1]+19, 36, WHITE, True)

def _app_dashboard(dst, app_selected=0, store_apps=None, store_selected=0, message=""):
    _panel(dst, (38, 445, 710, 342), "Aplicações")
    # Sidebar
    labels = [("🎮", "Jogos"), ("🔧", "Ferramentas"), ("★", "Favoritos"), ("⬇", "Instaladas")]
    for i, (symbol, label) in enumerate(labels):
        y = 520 + i*58
        if i == app_selected:
            _rounded(dst, (54,y,350,58), (160,65,0), (255,165,0), 13, 3, True)
        _text(dst, symbol, 77, y+8, 33, WHITE if i==app_selected else GOLD, True)
        _text(dst, label, 160, y+11, 25, WHITE, True)
    # Controller illustration card
    _rounded(dst, (420, 505, 300, 264), (8,7,6), (100,55,18), 20, 2)
    _text(dst, "🎮", 570, 555, 110, ORANGE, True, True)
    _text(dst, "Joga os teus jogos\nfavoritos no PiFootball!", 570, 690, 21, WHITE, True, True)
    # Right install panel
    _panel(dst, (765, 445, 845, 342), "Instalar Apps", "⬇")
    apps = store_apps or [
        ("YouTube", "Vídeos e transmissões", "▶", (235,0,0)),
        ("WhatsApp", "Mensagens e chamadas", "◉", (0,190,70)),
        ("Discord", "Fala com os teus amigos", "◉", (75,85,235)),
        ("IPTV Player", "Canais IPTV gratuitos", "▣", (115,100,90))
    ]
    for i, app in enumerate(apps[:4]):
        if len(app) >= 4:
            name, desc, symbol, color = app[:4]
        else:
            name, desc = app[0], app[1]
            symbol, color = "▣", (100,100,100)
        y = 516 + i*64
        if i == store_selected:
            pygame.draw.rect(dst, (90,50,10), (785,y-4,810,60), border_radius=12)
        pygame.draw.line(dst, (65,53,40), (785,y+57), (1590,y+57), 1)
        pygame.draw.rect(dst, color, (800,y,65,51), border_radius=14)
        _text(dst, symbol, 832, y+8, 30, WHITE, True, True)
        _text(dst, name, 918, y+2, 24, WHITE, True)
        _text(dst, desc, 918, y+31, 17, MUTED)
        _rounded(dst, (1440,y+1,155,47), (8,8,8), (255,100,0), 14, 2)
        _text(dst, "Instalar", 1518, y+9, 21, WHITE, True, True)

def render(screen, page="home", selected=0, app_selected=0, store_selected=0,
           store_apps=None, active_profile="Utilizador", message=""):
    """Render the themed interface, keeping the existing input and app logic."""
    canvas = pygame.Surface((BASE_W, BASE_H))
    _background(canvas)
    _header(canvas, selected)
    _nav(canvas, selected)
    if page in ("home", "apps", "store"):
        _app_dashboard(canvas, app_selected, store_apps, store_selected, message)
        if page == "store":
            _text(canvas, "LOJA COMPLETA — seleciona uma aplicação e carrega OK", 55, 795, 17, GOLD, True)
    else:
        title = {
            "tv":"TV & IPTV", "iptv":"CONFIGURAR IPTV", "browser":"INTERNET / NAVEGADOR",
            "settings":"DEFINIÇÕES", "users":"UTILIZADORES"
        }.get(page, page.upper())
        _panel(canvas, (55, 450, 1560, 335), title, "▣")
        _text(canvas, "Perfil ativo: " + active_profile, 95, 530, 24, GOLD, True)
        _text(canvas, message or "Utiliza as setas e OK para navegar.", 95, 590, 22, WHITE)
        _text(canvas, "O conteúdo e as opções mantêm-se ligados às funções existentes do sistema.", 95, 650, 18, MUTED)
    _footer(canvas, message if page != "home" else "")
    w, h = screen.get_size()
    scaled = pygame.transform.smoothscale(canvas, (w, h))
    screen.blit(scaled, (0, 0))
