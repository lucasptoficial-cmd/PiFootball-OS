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
- HOME: setas para navegar, Enter para abrir e Esc para sair.
- Definições: setas para escolher, Enter para alterar a animação ou abrir a gestão de utilizadores, Esc para voltar.
- Utilizadores: setas para trocar de perfil, escrever um nome e Enter para criar/selecionar, F2 para apagar o perfil ativo (mantém sempre pelo menos um).
- IPTV: setas/Tab para mudar de campo e Enter no último campo para guardar.

Os perfis e a preferência da animação são guardados localmente em `~/.config/pifootball/`. Não existe sincronização na nuvem nem isolamento de ficheiros por utilizador nesta fase.

O ecrã IPTV permite preencher e guardar host/IP, porta, utilizador e URL M3U de um fornecedor autorizado; ainda não estabelece ligação nem reproduz canais. A palavra-passe permanece apenas na memória da sessão e não é guardada.

A imagem `.img` será preparada depois de a base ser testada num Raspberry Pi 2 real.
