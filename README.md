# PiFootball OS

Sistema multimédia para Raspberry Pi 2 Model B (32-bit ARM).

**Estado:** protótipo inicial; ainda não é uma imagem de sistema pronta.

## Hardware-alvo
- Raspberry Pi 2 Model B, 1 GB RAM, ARMv7
- Raspberry Pi OS Lite 32-bit
- HDMI e teclado/controlo USB

## Executar
1. Instalar Raspberry Pi OS Lite (32-bit).
2. Clonar este repositório.
3. Executar `bash scripts/install.sh`.
4. Iniciar com `bash scripts/run.sh`.

## Controlos
Setas para navegar, Enter para selecionar e Esc para sair.

A aplicação IPTV está prevista como funcionalidade integrada: configuração de host/IP, porta, utilizador, palavra-passe e listas M3U/Xtream de fornecedores autorizados. Ainda não está implementada.

A imagem `.img` será preparada depois de a base ser testada num Raspberry Pi 2 real.
