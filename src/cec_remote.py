"""Entrada HDMI-CEC para o comando da televisão Samsung.

Usa cec-client (pacote cec-utils) e converte teclas CEC em eventos Pygame.
O botão Select/OK só seleciona ao ser libertado; mantê-lo 5 segundos abre HOME.
"""
import re
import shutil
import subprocess
import threading
import time

KEYS = {
    "up": "up", "down": "down", "left": "left", "right": "right",
    "select": "select", "enter": "select",
    "root menu": "home", "exit": "back", "back": "back",
    "channel up": "channel_up", "channel down": "channel_down",
    "page up": "channel_up", "page down": "channel_down",
}

class SamsungRemote:
    def __init__(self, pygame, home_event_type, ok_hold_seconds=5.0):
        self.pygame = pygame
        self.home_event_type = home_event_type
        self.ok_hold_seconds = ok_hold_seconds
        self.process = None
        self.thread = None
        self.stopping = threading.Event()
        self.ok_started = None
        self.last_key = None

    def start(self):
        executable = shutil.which("cec-client")
        if not executable:
            raise RuntimeError("cec-client não encontrado; instala cec-utils")
        self.process = subprocess.Popen(
            [executable, "-d", "8"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1
        )
        self.thread = threading.Thread(target=self._read, daemon=True)
        self.thread.start()

    def _post_key(self, name):
        pg = self.pygame
        mapping = {
            "up": pg.K_UP, "down": pg.K_DOWN,
            "left": pg.K_LEFT, "right": pg.K_RIGHT,
            "back": pg.K_ESCAPE, "channel_up": pg.K_PAGEUP,
            "channel_down": pg.K_PAGEDOWN,
        }
        key = mapping.get(name)
        if key is not None:
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=key, unicode=""))

    def _read(self):
        pattern = re.compile(r"key\s+(pressed|released):\s*(.*?)\s*\(", re.I)
        while not self.stopping.is_set() and self.process and self.process.stdout:
            line = self.process.stdout.readline()
            if not line:
                break
            match = pattern.search(line)
            if not match:
                continue
            action, raw_name = match.groups()
            name = KEYS.get(raw_name.strip().lower())
            if not name:
                continue
            if action.lower() == "pressed":
                if name == "select":
                    if self.ok_started is None:
                        self.ok_started = time.monotonic()
                elif name not in ("home",):
                    self._post_key(name)
            elif name == "select" and self.ok_started is not None:
                elapsed = time.monotonic() - self.ok_started
                self.ok_started = None
                if elapsed >= self.ok_hold_seconds:
                    self.pygame.event.post(self.pygame.event.Event(self.home_event_type))
                else:
                    self.pygame.event.post(self.pygame.event.Event(
                        self.pygame.KEYDOWN, key=self.pygame.K_RETURN, unicode=""))
            elif name == "home":
                self.pygame.event.post(self.pygame.event.Event(self.home_event_type))

    def stop(self):
        self.stopping.set()
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
