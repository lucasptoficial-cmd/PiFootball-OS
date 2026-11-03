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

## Multijogador — capacidade por mapa

- Limite definido: **7 jogadores no total por mapa**, incluindo quem criou/acolhe a sessão.
- Ao atingir 7 jogadores, novas entradas nesse mapa devem ser recusadas; outros mapas podem ter as suas próprias sessões.
- Configuração: `apps/picraft/multiplayer.json` (`max_players_per_map: 7`).
- Este valor fica definido como requisito/configuração do PiCraft; a implementação de rede e o bloqueio efetivo de entradas dependem da integração do motor multiplayer e ainda não estão concluídos.
