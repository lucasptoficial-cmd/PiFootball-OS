"""PiCraft 3D - base Ursina com controlos N'PLAY via recetor USB."""
import json, os
from pathlib import Path
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

try:
    import pygame
    pygame.joystick.init()
except Exception:
    pygame = None

BASE = Path(__file__).resolve().parent
os.chdir(BASE)
PROFILE = BASE / "player_profile.json"
profile = {"nick": "Jogador", "skin_path": "", "voice_chat_enabled": False}
if PROFILE.exists():
    try: profile.update(json.loads(PROFILE.read_text(encoding="utf-8")))
    except Exception: pass

# IDs SDL comuns em comandos PC/PS3. Recetores diferentes podem trocar índices.
BTN = {"A": 0, "Y": 3, "L1": 4, "R1": 5, "START": 9, "L3": 10, "R3": 11}
AXIS = {"LX": 0, "LY": 1, "RX": 2, "RY": 3, "L2": 4, "R2": 5}

app = Ursina(title="PiCraft 3D")
window.fps_counter.enabled = True
window.exit_button.visible = True
WORLD = 10
BLOCKS = [
    ("Relva", color.rgb(92, 160, 76)), ("Pedra", color.rgb(125, 130, 137)),
    ("Terra", color.rgb(130, 86, 54)), ("Madeira", color.rgb(150, 104, 61)),
    ("Areia", color.rgb(218, 199, 133)), ("Cristal", color.rgb(105, 190, 205))
]
selected = 0
voxels = []
game = {"active": False, "player": None, "pad": None, "last": {},
        "chat": False, "inventory": False, "hud": None, "chat_text": []}
menu = Entity(parent=camera.ui)
Text(parent=menu, text="PiCraft 3D", y=.32, scale=2, origin=(0, 0), color=color.lime)
Text(parent=menu, text="N'PLAY Skill 8.1 / 2.1 • PC/PS3 USB receiver", y=.22, scale=.8, origin=(0, 0))
start_btn = Button(parent=menu, text="Jogar", y=.05, scale=(.25, .08), color=color.azure)

def hud_text():
    return f"{BLOCKS[selected][0]} | R2 partir · L2 colocar · L1/R1 itens · Y inventário · A saltar · L3 correr · R3 agachar · START menu · ↑ chat"

def make_world():
    for x in range(WORLD):
        for z in range(WORLD):
            voxels.append(Entity(model="cube", position=(x, 0, z), color=BLOCKS[0][1], collider="box"))
            voxels.append(Entity(model="cube", position=(x, -1, z), color=BLOCKS[2][1], collider="box"))

def get_pad():
    if not pygame: return None
    try:
        pygame.event.pump()
        if pygame.joystick.get_count() == 0: return None
        p = pygame.joystick.Joystick(0)
        if not p.get_init(): p.init()
        return p
    except Exception: return None

def button(name):
    p = game["pad"]
    if not p: return False
    try:
        if name in ("L2", "R2"):
            axis = p.get_axis(AXIS[name])
            return axis > .55
        return bool(p.get_button(BTN[name]))
    except Exception: return False

def edge(name, action):
    now = button(name)
    before = game["last"].get(name, False)
    game["last"][name] = now
    if now and not before: action()

def ray_block():
    hit = raycast(camera.world_position, camera.forward, distance=5)
    return hit if hit.hit and hit.entity in voxels else None

def attack():
    hit = ray_block()
    if hit:
        voxels.remove(hit.entity)
        destroy(hit.entity)

def place():
    hit = ray_block()
    if hit:
        pos = hit.entity.position + hit.normal
        block = Entity(model="cube", position=pos, color=BLOCKS[selected][1], collider="box")
        voxels.append(block)

def cycle(direction):
    global selected
    selected = (selected + direction) % len(BLOCKS)
    if game["hud"]: game["hud"].text = hud_text()

def toggle_inventory():
    game["inventory"] = not game["inventory"]
    if game["inventory"]:
        game["inventory_ui"] = Text(parent=camera.ui,
            text="INVENTÁRIO\n" + "\n".join(f"{i+1}. {b[0]}" for i,b in enumerate(BLOCKS)) + "\n\nY para fechar",
            origin=(0,0), background=True, scale=1.2)
        mouse.locked = False
    else:
        if game.get("inventory_ui"): destroy(game["inventory_ui"])
        game["inventory_ui"] = None
        mouse.locked = True

def open_chat():
    if game["chat"]: return
    game["chat"] = True
    game["chat_input"] = InputField(parent=camera.ui, default_value="", position=(-.4,-.43), scale=(.8,.06))
    mouse.locked = False

def finish_chat():
    field = game.get("chat_input")
    if field and field.text.strip():
        game["chat_text"].append(profile["nick"] + ": " + field.text.strip())
        game["chat_text"] = game["chat_text"][-3:]
        game["hud"].text = hud_text() + "\n" + "\n".join(game["chat_text"])
        field.text = ""
    if field: destroy(field)
    game["chat_input"] = None
    game["chat"] = False
    mouse.locked = True

def start_game():
    if game["active"]: return
    menu.enabled = False
    game["active"] = True
    make_world()
    game["player"] = FirstPersonController(position=(WORLD/2, 3, WORLD/2))
    game["player"].speed = 5
    game["pad"] = get_pad()
    game["hud"] = Text(parent=camera.ui, text=hud_text(), position=(-.86,.47), scale=.7)
    mouse.locked = True
    print("Comando:", game["pad"].get_name() if game["pad"] else "não detetado; liga a pen USB")

def back_menu():
    game["active"] = False
    for obj in voxels: destroy(obj)
    voxels.clear()
    if game["player"]: destroy(game["player"])
    if game["hud"]: destroy(game["hud"])
    game["player"] = game["hud"] = None
    game["pad"] = None
    game["last"].clear()
    menu.enabled = True
    mouse.locked = False

start_btn.on_click = start_game

def update():
    if not game["active"]: return
    if not game["pad"]: game["pad"] = get_pad()
    p = game["pad"]
    if not p: return
    try:
        pygame.event.pump()
        player = game["player"]
        # Analógico direito desloca o jogador; esquerdo roda a câmara.
        rx, ry = p.get_axis(AXIS["RX"]), p.get_axis(AXIS["RY"])
        lx, ly = p.get_axis(AXIS["LX"]), p.get_axis(AXIS["LY"])
        if abs(rx) > .16: player.position += player.right * rx * time.dt * 5
        if abs(ry) > .16: player.position += player.forward * -ry * time.dt * 5
        player.rotation_y += lx * time.dt * 110
        player.camera_pivot.rotation_x = clamp(player.camera_pivot.rotation_x - ly * time.dt * 90, -80, 80)
        edge("A", lambda: setattr(player, "jump", True))
        edge("Y", toggle_inventory)
        edge("L1", lambda: cycle(-1))
        edge("R1", lambda: cycle(1))
        edge("R2", attack)
        edge("L2", place)
        edge("START", back_menu)
        player.speed = 8 if button("L3") else 5
        # R3 funciona como Shift/agachar enquanto está premido.
        player.height = 1.2 if button("R3") else 2
        player.camera_pivot.y = 1.2 if button("R3") else 2
        if p.get_numhats() and p.get_hat(0)[1] == 1 and not game["last"].get("CHAT", False):
            open_chat()
            game["last"]["CHAT"] = True
        elif not (p.get_numhats() and p.get_hat(0)[1] == 1):
            game["last"]["CHAT"] = False
    except Exception as exc:
        print("Leitura do comando falhou:", exc)

def input(key):
    if not game["active"]: return
    if game["chat"] and key == "enter":
        finish_chat()
    elif key == "escape":
        if game["chat"]: finish_chat()
        elif game["inventory"]: toggle_inventory()
        else: back_menu()
    elif key == "e": toggle_inventory()
    elif key == "enter": open_chat()
    elif key == "left mouse down": attack()
    elif key == "right mouse down": place()
    elif key in ("1","2","3","4","5","6"):
        global selected
        selected = int(key)-1
        game["hud"].text = hud_text()

app.run()
