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


### Roblox — verificação de arquitetura

A loja apresenta Roblox como experimental e faz uma verificação local da arquitetura antes de qualquer tentativa. No Raspberry Pi 2 (ARMv7/32-bit), bloqueia a tentativa porque os runtimes comunitários investigados exigem x86-64 ou, no caso do Cordial, no máximo aarch64 em desenvolvimento; ARMv7 não está suportado. Não existe um pacote otimizado que transforme o binário Android ARM64/x86-64 num programa ARMv7. Reduzir efeitos ou serviços do PiFootball OS não resolve a incompatibilidade de ABI. A Roblox também declara que Linux não é suportado oficialmente.

### PiTube — interface YouTube para televisão

Foi adicionada `apps/pitube/index.html`, uma interface TV própria com navegação para Início, Explorar, Shorts, Subscrições, Biblioteca, pesquisa e canais. A pesquisa e a reprodução são encaminhadas para páginas oficiais do YouTube; a interface não extrai streams nem substitui o leitor oficial. O PiTube precisa de um browser compatível (preferencialmente Chromium). A compatibilidade e o desempenho no Raspberry Pi 2 ainda não foram testados em hardware.

## PiCraft e PiModCraft (primeira versão)

A Loja de aplicações inclui agora duas aplicações locais:

- **PiCraft** (`apps/picraft/index.html`): gestor auxiliar de perfis, configuração de versão/loader, pré-visualização de skins PNG e atalhos para ferramentas/modpacks. Ainda não substitui um launcher oficial nem inicia o jogo por si só.
- **PiModCraft** (`apps/pimodcraft/index.html`): pesquisa mods no catálogo público Modrinth, filtra por loader e versão e permite descarregar ficheiros publicados. A instalação automática numa instância ainda não está implementada; é necessário colocar o `.jar` na pasta `mods` e instalar dependências.

As duas aplicações abrem pelo menu APLICAÇÕES → Loja de aplicações, usando o navegador disponível. A pesquisa Modrinth necessita de Internet e de um navegador com suporte a JavaScript moderno. A compatibilidade com Raspberry Pi 2/ARMv7 não está garantida; Minecraft moderno e modpacks podem exceder os recursos do equipamento.

## PiCraft — jogo voxel independente (protótipo 0.1)

O PiCraft está a evoluir para um jogo próprio, sem depender do Minecraft oficial. Foi criado `apps/picraft/game.html`, um primeiro protótipo jogável com:
- mundo voxel/isométrico gerado localmente;
- seis materiais originais (relva, terra, rocha, madeira, areia e cristal), com paletas e texturas desenhadas pelo próprio jogo;
- movimento por setas/WASD e controlos tácteis;
- seleção de blocos, colocação e remoção;
- inventário simples e efeitos sonoros sintetizados localmente;
- gravação do mundo no armazenamento local do navegador.

Abrir PiCraft e escolher **Jogar PiCraft**. Esta é uma base inicial 2D isométrica, não um motor 3D completo: ainda faltam primeira pessoa, crafting, ferramentas, mobs, iluminação, água, áudio gravado, mundos grandes e integração completa com o comando Samsung. Os sons são gerados por síntese e as texturas são originais, não recursos extraídos de outros jogos. O desempenho e os controlos têm de ser testados no Raspberry Pi 2 real.


### PiCraft 0.2 — conteúdo adicional nos ficheiros

- 56 blocos/materiais originais definidos no jogo.
- Inventário rolável para consultar o catálogo completo.
- Oito receitas iniciais de crafting.
- Dez tipos de criaturas com aparecimento durante a exploração e movimento simples.
- O mundo guarda também o estado das criaturas no armazenamento local do navegador.
- Continua a ser um protótipo isométrico 2D: não há ainda combate, drops, IA avançada ou bancada de crafting completa.
- Alterações feitas apenas em `apps/picraft/game.html` e documentação. Não foi criada nem alterada qualquer release ou imagem `.img`.


## Atualizações e recuperação de versão

Ao iniciar com `bash scripts/run.sh`, o sistema procura atualizações no GitHub. Se existir uma versão mais recente, pergunta se queres atualizar; responder `s` instala-a e qualquer outra resposta mantém a versão atual.

Para regressar à versão imediatamente anterior:
```bash
bash scripts/rollback.sh
```
O rollback também pede confirmação. O atualizador só faz atualizações diretas (fast-forward) e recusa atualizar ou reverter quando deteta alterações locais, para evitar apagá-las. A versão anterior fica guardada localmente em `.git`; é necessário ter instalado o sistema através de um clone Git e ter ligação à Internet para procurar atualizações. Não é um atualizador automático em segundo plano.
