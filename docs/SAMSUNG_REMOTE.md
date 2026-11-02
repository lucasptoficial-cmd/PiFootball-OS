# Comando Samsung por HDMI-CEC

## Estado

A primeira ponte de entrada foi criada em `src/cec_remote.py`. O processo lê eventos do `cec-client` e envia eventos Pygame para a interface.

Mapeamento implementado:
- Setas: navegação.
- Select/OK: seleciona quando o botão é libertado.
- OK mantido durante 5 segundos: regressa ao HOME.
- Back/Exit: regressa ao ecrã anterior.
- Channel Up/Down: envia PageUp/PageDown; o guia ainda não está implementado.

## Preparação da televisão

1. Ligar o Raspberry Pi diretamente a uma entrada HDMI da Samsung.
2. Ativar Anynet+ (HDMI-CEC) nas definições da televisão, se disponível.
3. Instalar o sistema e executar o instalador do PiFootball OS.
4. Reiniciar a televisão e o Raspberry Pi se não houver deteção CEC.

## Diagnóstico no Raspberry Pi

Executar:

```bash
cec-client -l
```

Depois:

```bash
echo 'scan' | cec-client -s -d 1
```

Os nomes dos botões e o comportamento podem variar com o modelo da televisão, firmware, porta HDMI e adaptador CEC. O comando Samsung ainda precisa de ser testado na TQ55S90DAE real.

## Limitações atuais

- O guia de canais ainda não existe.
- CH+/CH− são apenas encaminhados como eventos PageUp/PageDown.
- Não há controlo de volume, microfone ou teclas especiais nesta fase.
- A ponte depende de o kernel/adaptador HDMI expor o dispositivo CEC ao `cec-client`.
- Esta integração não prova compatibilidade até ser testada no hardware de destino.
