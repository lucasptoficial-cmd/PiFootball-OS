# Roteiro de desenvolvimento

## Etapa 1 — Base
- [x] Repositório e estrutura inicial
- [x] Interface navegável por teclado
- [x] Animação de arranque (preto, reflexo verde, logótipo, feixe de luz e transição laranja)
- [x] Ecrã inicial de configuração IPTV (host, porta, utilizador e URL M3U)
- [ ] Redesenhar o HOME final com os 8 blocos e identidade visual premium
- [x] Primeira integração HDMI-CEC: descodificador de teclas Samsung via cec-client e atalho OK mantido 5 segundos para HOME
- [x] Criar menu TV & IPTV com entrada para configuração e guia ainda indisponível
- [ ] Testar a integração HDMI-CEC com a Samsung TQ55S90DAE e o Raspberry Pi 2 físico
- [ ] Testar a animação, perfis e interface no Raspberry Pi 2 físico
- [ ] Arranque automático da interface

## Etapa 2 — Sistema
- [x] Perfis locais: criar, selecionar, alternar e apagar (mantendo pelo menos um)
- [x] Definição persistente para ativar/desativar animação de arranque
- [ ] Definições de imagem, som, rede e controlos
- [ ] Atualizações com confirmação do utilizador

## Etapa 3 — Conteúdo
- [ ] IPTV: ligação real a serviços autorizados, autenticação segura e reprodução
- [ ] Suporte Xtream Codes e M3U/M3U8 completo
- [ ] Futebol: resultados e calendário com fontes permitidas
- [ ] TV: canais e streams oficiais
- [ ] Aplicações compatíveis com ARM 32-bit
- [ ] Música e rádio

## Etapa 4 — Imagem
- [ ] Construção de imagem Raspberry Pi OS Lite 32-bit
- [ ] Testes reais de arranque e desempenho
- [ ] Expansão automática da partição no cartão microSD
