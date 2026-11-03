# PiCraft — critérios de instalação

O motor de terceiros é **Minecraft: Python Edition**, de pythonengineer:
https://github.com/pythonengineer/minecraft-python

## Critérios verificados/apresentados pelo instalador

- Python 3.9 ou superior.
- Ambiente gráfico com OpenGL funcional.
- Internet para obter dependências.
- Dependências do motor: Pyglet 1.5.x, Cython, Pillow, NumPy, PyOgg e nbtlib.
- wxPython é opcional.
- O projeto compila extensões Cython. ARMv7/32-bit é experimental e pode falhar.
- Raspberry Pi 2 Model B com 1 GB RAM está abaixo do recomendado para compilar e executar este motor; não há garantia de desempenho.

O instalador pede aceitação explícita da licença BSD 3-Clause antes de prosseguir. Nesta fase, apenas apresenta os critérios e verifica a versão de Python; não instala nem compila ainda o motor. Não declares compatibilidade como confirmada sem testes no equipamento.
