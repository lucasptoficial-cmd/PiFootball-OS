"""Suporte a comandos NPlay Skill 8.1 e Skill 2.1 através de USB/Bluetooth HID.

Os dois modelos usam a interface de comando normal do Linux/Pygame:
- Skill 8.1 (NGG4334BK): sem fios, PC/PS3.
- Skill 2.1 (NWC8575BK): com fios, PC/PS3.

Não instala firmware proprietário. A compatibilidade depende do modo USB,
do kernel e de o comando aparecer como dispositivo joystick.
"""
import pygame


class NPlayGamepads:
    """Traduz comandos HID NPlay e outros gamepads para teclas da interface."""

    def __init__(self, pygame_module):
        self.pg = pygame_module
        self.devices = {}
        self.last_axis = {}
        self.status = "NPlay: à espera de comando"
        self._initialise_existing()

    def _initialise_existing(self):
        try:
            self.pg.joystick.init()
            for index in range(self.pg.joystick.get_count()):
                self._add(index)
        except pygame.error as exc:
            self.status = "Gamepad indisponível: " + str(exc)

    def _add(self, index):
        try:
            joy = self.pg.joystick.Joystick(index)
            joy.init()
            name = joy.get_name()
            self.devices[joy.get_instance_id()] = joy
            upper = name.upper()
            if "NGG4334" in upper or ("NPLAY" in upper and "8.1" in upper):
                model = "NPlay Skill 8.1"
            elif "NWC8575" in upper or ("NPLAY" in upper and "2.1" in upper):
                model = "NPlay Skill 2.1"
            elif "NPLAY" in upper:
                model = "NPlay"
            else:
                model = "Comando HID"
            self.status = model + " ligado: " + name[:42]
        except pygame.error as exc:
            self.status = "Erro ao ligar comando: " + str(exc)

    def _remove(self, instance_id):
        joy = self.devices.pop(instance_id, None)
        if joy:
            try:
                joy.quit()
            except pygame.error:
                pass
        self.status = "NPlay: comando desligado" if not self.devices else "Comando ligado"

    def _key(self, key):
        self.pg.event.post(self.pg.event.Event(
            self.pg.KEYDOWN, key=key, unicode="", mod=0
        ))

    def handle_event(self, event):
        """Recebe eventos JOY* do ciclo principal e envia teclas Pygame."""
        if event.type == self.pg.JOYDEVICEADDED:
            self._add(event.device_index)
            return
        if event.type == self.pg.JOYDEVICEREMOVED:
            self._remove(event.instance_id)
            return

        if event.type == self.pg.JOYHATMOTION:
            x, y = event.value
            if x:
                self._key(self.pg.K_RIGHT if x > 0 else self.pg.K_LEFT)
            if y:
                self._key(self.pg.K_UP if y > 0 else self.pg.K_DOWN)
            return

        if event.type == self.pg.JOYAXISMOTION:
            # Analógico esquerdo: eixos 0 e 1; zona morta evita movimentos acidentais.
            axis = event.axis
            if axis not in (0, 1):
                return
            value = event.value
            direction = 0 if abs(value) < 0.55 else (1 if value > 0 else -1)
            previous = self.last_axis.get((event.instance_id, axis), 0)
            if direction != previous:
                self.last_axis[(event.instance_id, axis)] = direction
                if direction:
                    if axis == 0:
                        self._key(self.pg.K_RIGHT if direction > 0 else self.pg.K_LEFT)
                    else:
                        self._key(self.pg.K_DOWN if direction > 0 else self.pg.K_UP)
            return

        if event.type == self.pg.JOYBUTTONDOWN:
            # Mapeamento HID/XInput habitual: botão 0 confirma, 1/6 volta.
            if event.button in (0, 7):
                self._key(self.pg.K_RETURN)
            elif event.button in (1, 6):
                self._key(self.pg.K_ESCAPE)
            elif event.button == 3:
                self._key(self.pg.K_PAGEUP)
            elif event.button == 4:
                self._key(self.pg.K_PAGEDOWN)

    def close(self):
        for joy in list(self.devices.values()):
            try:
                joy.quit()
            except pygame.error:
                pass
        self.devices.clear()
