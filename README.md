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


### Loja: atalhos Web

A loja inclui atalhos para YouTube, WhatsApp Web, Instagram e Discord Web, além de pacotes Linux (NetSurf, VLC e Audacious). Os atalhos abrem no navegador externo instalado; não são aplicações nativas nem garantem compatibilidade com o browser antigo do Raspberry Pi 2. Roblox aparece apenas como informação de incompatibilidade: não existe cliente oficial para Linux. A interface e os atalhos ainda precisam de testes no hardware.


### YouTube como aplicação

A entrada YouTube tenta abrir o Chromium em modo `--app=https://www.youtube.com`, numa janela dedicada, se o Chromium estiver instalado; caso contrário, usa o navegador disponível. Isto é uma aplicação Web em janela própria, não um cliente oficial nativo do YouTube. O Raspberry Pi 2 (ARMv7/32-bit, 1 GB RAM) pode ter limitações importantes de desempenho e reprodução; testar no equipamento é obrigatório.

### Roblox no Linux — investigação

A Roblox declara oficialmente que o cliente não é suportado em Linux. Foram encontrados projetos comunitários como Sober e TuxBlox, mas os requisitos publicados são incompatíveis com o Raspberry Pi 2: Sober requer x86_64/SSE4.2 e TuxBlox indica x86-64, 8 GB RAM e kernel Linux recente. Portanto, Roblox fica catalogado como não compatível com este hardware, sem botão de instalação enganador.
