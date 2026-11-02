# Comandos NPlay Skill 8.1 e 2.1

## Modelos previstos

- **NPlay Skill 8.1 (NGG4334BK):** comando sem fios para PC/PS3.
- **NPlay Skill 2.1 (NWC8575BK):** comando com fios para PC/PS3.

O PiFootball OS usa a interface de joystick USB/HID do Pygame/Linux. Não instala firmware proprietário nem depende de software Windows da NPlay.

## Controlos

- D-pad ou analógico esquerdo: navegar.
- Botão principal (mapeamento HID habitual, botão 0): OK/confirmar.
- Botão secundário (habitualmente botão 1): BACK/voltar.
- Botões 3 e 4: Page Up / Page Down, quando presentes.

O mapeamento pode variar conforme o modo PC/PS3 e a forma como o kernel identifica o comando. Se os botões não corresponderem, será necessário ajustar o perfil ao identificador HID real.

## Como ligar

1. Ligar o Skill 2.1 por USB.
2. Ligar o Skill 8.1 por USB ou emparelhá-lo por Bluetooth no Raspberry Pi.
3. Confirmar que o Linux o apresenta como joystick.
4. Abrir o PiFootball OS. O estado do comando aparece na barra inferior do HOME.

## Limitações

A integração foi adicionada ao código, mas ainda não foi testada fisicamente com os dois modelos. A deteção depende do suporte HID do kernel, do adaptador Bluetooth/USB e da versão do Pygame instalada.