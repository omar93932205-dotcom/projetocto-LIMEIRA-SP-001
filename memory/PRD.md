# PRD — donas-projector-pcma-cebaspe-002

## Overview
Existing project cloned from GitHub (https://github.com/cicijevaira-sys/donas-projector-pcma-cebaspe-002)
and configured in the Emergent sandbox (/app). Public inscription/tracking site (Cebraspe / PCMA concurso)
with an admin panel for tracking, inscriptions, dashboard KPIs and PIX config.

## Stack
- Backend: FastAPI (Python) — /app/backend (server.py + admin_routes.py + pix_generator.py)
- Frontend: React CRA (craco) — /app/frontend
- DB: MongoDB (MONGO_URL / DB_NAME from /app/backend/.env — unchanged)

## Setup done (2026-06 / clone date 2026-08-25 in sandbox)
- Cloned repo into /app, preserving .git, .emergent, backend/.env, frontend/.env
- Backend deps installed (requirements.txt; emergentintegrations not present — no skip needed). Extras bcrypt/Pillow/qrcode[pil] already satisfied.
- Frontend deps installed via yarn
- Seeded admin `farpa` (bcrypt) into `admins` collection
- Services restarted via supervisor (backend + frontend)

## Key routes
- GET /api/ -> health ({"message":"Painel Administrativo API"})
- POST /api/admin/auth/login -> returns JWT { token, user }
- Admin UI SPA route: /farpapainel

## Validation status (passed)
- GET /api/ -> 200
- Frontend root -> 200, renders concurso landing page
- POST /api/admin/auth/login {farpa/Ads102030} -> JWT returned

## Notes
- Preview serves frontend via hot-reload dev server; production `yarn build` not required for preview.
- JWT_SECRET defaults to 'change-me' (env-overridable). Consider setting ADMIN/JWT env in production.

## Regras do concurso SESAU_AL_26 (memorizar)
- Taxa de inscrição: Nível SUPERIOR (Especialista, cargos 01-12) = R$ 160,00 | Nível MÉDIO (Assistente, cargos 13-15) = R$ 120,00
- Estes valores estão nos data-price das options do #VAGA em dados-inscricao.html e alimentam a geração do pagamento (PIX).
- Localidade de Vaga: CARGO 1 (Biologia) -> só Maceió; CARGO 2-15 -> Arapiraca, Delmiro Gouveia, Maceió, Palmeira dos Índios, Porto Calvo, União dos Palmares.
- Local de prova: estado Alagoas/AL (fixo); municípios Arapiraca/AL e Maceió/AL.
- Período de inscrições: 20/07/2026 a 26/08/2026 às 23:59.

## Rebrand completo PC_MA_26 -> SESAU_AL_26 (todas as telas)
Data: sessão de migração.
Páginas públicas (7) migradas: inicio.html, termos.html, inscricao.html, dados-inscricao.html, confirmacao.html, inscricao-realizada.html, pagamento-pix.html (tela + documento de impressão).
Painel admin (/donaspainel) rebrandeado: bundle main.fda9cfa5.js ('Concurso PC MA 26' -> 'Concurso SESAU AL 26'), index.html title, donaspainel-documentos.html title ('Polícia Penal RN' -> 'Documentos - Painel Cebraspe').
Backend (admin_routes.py): PIX defaults pix_nome='CONCURSO ALAGOAS', pix_cidade='MACEIO AL'; telegram_titulo fallback 'NOVA INSCRIÇÃO - SESAU AL 26'; fallbacks 'IDECAN'->'CONCURSO ALAGOAS', 'BELO HORIZONTE'->'MACEIO AL'.
DB settings corrigidas: pix_cidade 'Marceio AL' -> 'MACEIO AL'.
Regras: taxa superior (cargos 01-12) R$160,00; médio (13-15) R$120,00. Localidade de Vaga: CARGO 1 só Maceió; demais 6 cidades. Local de prova AL (Arapiraca/Maceió).
Identificadores JS internos window.IdecanNotice/IdecanConfirm mantidos (nomes internos, não visíveis ao usuário).
Verificado por testing_agent (iterations 10-13): 100% backend e frontend.
Pendências/observações: imagem decorativa do login do painel (Tartaruga Ninja) é um asset off-brand — aguardando decisão do usuário para trocar.

## Changelog — 2026-06 (fork: migração p/ Avança SP / Prefeitura de Limeira)
- Página inicial (`inicio.html`) substituída pela página "Avança SP" (SingleFile). Botão "Inscrição Online" → `/termos.html`. Todos os links externos (menu, área candidato, PDFs, proseleta) neutralizados para `#`.
- Cabeçalho e rodapé padrão Avança SP aplicados em TODAS as páginas do fluxo (`termos, dados-inscricao, inscricao, confirmacao, pagamento-pix, inscricao-realizada`), substituindo o header/footer Cebraspe (wrappers `__cebraspe_topbar_root`/`__cebraspe_footer_root`). Classes isoladas `av-*` para não colidir com CSS existente. Logo salvo em `/app/frontend/public/avanca-logo.jpg`.
- Títulos (`<title>`) das 6 páginas atualizados para "… | Avança SP".
- Script: `/app/scripts/apply_avanca_headerfooter.py`.
- PENDENTE (não solicitado ainda): conteúdo do corpo das páginas ainda menciona "SEAP-MA / Secretaria de Administração Penitenciária do Maranhão" — precisa migrar para contexto Prefeitura de Limeira quando o usuário pedir.

## Changelog — 2026-06 (títulos do concurso migrados)
- Título do concurso no CORPO das 6 páginas do fluxo trocado de "Concurso Público da Secretaria de Estado de Administração Penitenciária do Maranhão (SEAP_MA_26)" para "Concurso Público - 01/2026 - Prefeitura Municipal de Limeira" (h1, intro, subtítulos, var JS CONCURSO, edital, optgroups, copyright). Verificado pelo testing agent (iteration_14.json, frontend 100%).
- Script: /app/scripts/migra_titulos_limeira.py
- PENDENTE (localidades): estado da prova ainda "Maranhão / MA" em dados-inscricao.html (~l.877) e mapa {'MA':'Maranhão'} em confirmacao.html (~l.908). Migrar para São Paulo/SP na tarefa de localidades/cargos.

## Changelog — 2026-06 (cargos + taxas + local prova Limeira)
- `dados-inscricao.html`: select de VAGA agora tem 86 cargos da Prefeitura de Limeira em 4 optgroups por escolaridade — Médio(18), Médio + Técnico(11), Superior(34), Fundamental Completo(23). Cada option tem data-price: Fundamental 59.00, Médio/Médio+Técnico 79.00, Superior 98.00 (lista extraída da tabela VAGAS de inicio.html).
- Local de Prova: UF "São Paulo / SP" e Município "LIMEIRA / SP" (antes Maranhão/São Luís). JS force uf='SP'. Fallback de valor 180→98.
- `confirmacao.html`: mapa UF agora {'SP':'São Paulo','MA':'Maranhão'}.
- `pagamento-pix.html`: fallback de valor 180→98. Taxa (p-valor) vem do __valor do sessionStorage (data-price da vaga); backend calcula valor a partir de __taxa em admin_routes.py (~l.316), sem tabela SEAP hardcoded.
- Verificado ao vivo: lista/grupos/taxas e local da prova OK (screenshots + eval JS). p-valor recebe R$98 do contexto. Geração do QR PIX depende da chave PIX configurada no painel (config manual, fora do escopo desta tarefa).
- Script: /app/scripts/migra_cargos_limeira.py

## Changelog — 2026-06 (banner CONCURSOS no fluxo)
- Adicionado bloco "CONCURSOS" (barra cinza + brasão de Limeira + "Concurso Público" + título + "Inscrições de 31/07 a 31/08/2026") logo abaixo do cabeçalho em todas as 6 páginas do fluxo, SEM o botão "Inscrição Online" (esse só na home). Classe isolada `av-cbanner`. Brasão: /app/frontend/public/limeira-brasao.png. Script: /app/scripts/add_concurso_banner.py. Verificado por screenshot.

## Changelog — 2026-06 (alinhamento + limpeza título termos)
- termos.html: removido h1 redundante "Concurso Público - 01/2026 - Prefeitura Municipal de Limeira" (já aparece no banner). Mantido badge "Termos e Condições" + intro.
- Alinhamento unificado: banner av-cbanner e conteúdo agora 1140px/padding 30px em todas as 6 páginas. termos.html: `main .container` forçado a 1140/30px (style __align_v1). Verificado por screenshot (termos + dados-inscricao).

## Changelog — 2026-06 (remove duplicidade do concurso no corpo)
- Removido bloco duplicado do concurso no corpo das páginas (já consta no banner): inscricao/dados/confirmacao = card interno #TopoInformacoes (imagem+dados "Concurso"+título+período) removido mantendo o wrapper (tabela de confirmação intacta). pagamento-pix/inscricao-realizada = removido <h2> subtítulo (recibo do PIX preservado com o nome do concurso). Script: /app/scripts/remove_concurso_dup.py. Verificado por screenshot (inscricao.html).

## Changelog — 2026-06 (comprovante PIX / impressão corrigidos)
- pagamento-pix.html: @media print agora esconde .av-header/.av-topmenu/.av-topo/.av-cbanner/.av-footer/#__cebraspe_topbar_root/#__cebraspe_footer_root (impressão mostra SÓ o comprovante). #print-header rebrandizado: brasão /limeira-brasao.png + "Prefeitura Municipal de Limeira" + título concurso + "Avança SP — Gestão de Processos Seletivos Online" + "Comprovante de Pagamento PIX" (removido Cebraspe/Centro Brasileiro).
- DB settings.main: pix_nome='CONCURSO LIMEIRA', pix_cidade='LIMEIRA' (código PIX não mostra mais SEAP MA/SAO LUIS).
- admin_routes.py: fallbacks hardcoded 'CONCURSO SEAP MA'/'SAO LUIS MA' -> 'CONCURSO LIMEIRA'/'LIMEIRA' e título Telegram default -> 'NOVA INSCRIÇÃO - PREFEITURA DE LIMEIRA'.
- Verificado pelo testing agent (iteration_15.json): backend 100%, frontend 100% — impressão limpa, branding Limeira/Avança, código PIX com CONCURSO LIMEIRA.
