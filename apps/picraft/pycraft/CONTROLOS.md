# PiCraft 3D — N'PLAY Skill 8.1 / 2.1

Esta pasta contém a versão Python/Ursina do PiCraft. O comando é usado apenas dentro do jogo.

| Comando | Ação |
|---|---|
| R2 | Atacar / partir bloco |
| L2 | Colocar bloco |
| R1 / L1 | Próximo / anterior bloco |
| START | Menu (equivalente a Esc) |
| Y | Abrir/fechar inventário |
| A | Saltar |
| R3 | Agachar (Shift) enquanto premido |
| L3 | Correr enquanto premido |
| Analógico direito | Andar para a frente/trás e para os lados |
| Analógico esquerdo | Rodar a câmara |
| Cima no D-pad | Abrir chat |
| Enter | Enviar mensagem no chat |
| Esc | Fechar chat/inventário ou voltar ao menu |

## Recetor USB

Ligar a pen recetora antes de iniciar o jogo. O módulo usa SDL/Pygame para ler comandos reconhecidos pelo sistema. Não depende de Bluetooth.

## Atenção à primeira configuração

Os índices SDL variam entre recetores e modos de compatibilidade. O mapeamento inicial usa o layout mais comum em comandos PC/PS3:
- Botões: A=0, Y=3, L1=4, R1=5, START=9, L3=10, R3=11.
- Eixos: analógicos esquerdo=0/1, direito=2/3, L2=4, R2=5.

Se o comando for detetado mas os botões não corresponderem, executar `python -m pygame.examples.joystick` num PC para identificar os índices reais e ajustar `BTN`/`AXIS` no início de `main.py`.

## Instalação

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

**Estado:** mapeamento inicial preparado, ainda não testado com o N'PLAY físico nem no Raspberry Pi 2. Ursina/Panda3D pode ser demasiado pesado para o Pi 2; testar primeiro num PC e depois medir no Raspberry.
