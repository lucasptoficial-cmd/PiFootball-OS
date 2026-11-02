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
- HOME: setas para navegar, OK para abrir e BACK para voltar.
- TV & IPTV: abre um menu com configuração IPTV e entrada para o futuro guia de canais.
- HDMI-CEC: setas, OK, BACK e OK mantido 5 segundos para HOME; CH+/CH− são encaminhados como PageUp/PageDown.
- Definições: setas para escolher, Enter para alterar a animação ou abrir a gestão de utilizadores, Esc para voltar.
- Utilizadores: setas para trocar de perfil, escrever um nome e Enter para criar/selecionar, F2 para apagar o perfil ativo (mantém sempre pelo menos um).
- IPTV: setas/Tab para mudar de campo e Enter no último campo para guardar.
- Comando Samsung: entrada HDMI-CEC via `cec-client`; setas navegam, OK seleciona ao largar, OK mantido 5 segundos abre HOME, BACK volta. CH+/CH− são convertidos para teclas PageUp/PageDown para integração com o futuro guia de canais.

Os perfis e a preferência da animação são guardados localmente em `~/.config/pifootball/`. Não existe sincronização na nuvem nem isolamento de ficheiros por utilizador nesta fase.

O ecrã IPTV permite preencher e guardar host/IP, porta, utilizador e URL M3U de um fornecedor autorizado; ainda não estabelece ligação nem reproduz canais. A palavra-passe permanece apenas na memória da sessão e não é guardada.

A imagem `.img` será preparada depois de a base ser testada num Raspberry Pi 2 real.


## Browser e loja de aplicações (protótipo)

- O menu INTERNET abre um campo de endereço e tenta lançar o NetSurf, se estiver instalado.
- A secção APLICAÇÕES inclui a loja com NetSurf, VLC e Audacious como pacotes sugeridos.
- A instalação exige confirmação no ecrã e abre um terminal gráfico com `sudo apt-get` (ou usa `pkexec` se existir).
- São aplicações Linux dos repositórios configurados no Raspberry Pi OS, não APKs Android. A disponibilidade dos pacotes depende da versão e arquitetura do sistema.
- O browser é uma janela externa; ainda não está integrado dentro do PiFootball OS. A compatibilidade e desempenho têm de ser testados no Raspberry Pi 2.
