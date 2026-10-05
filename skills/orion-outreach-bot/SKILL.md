---
name: orion-outreach-bot
description: Use ao construir/operar o bot multicanal da Orion (seg–sex). Define arquitetura (n8n + Evolution API + SMTP + Postgres), comportamento, aprovação humana, opt-out e rate limit. Fase 5.
---

# orion-outreach-bot

Arquitetura e regras do bot de prospecção multicanal. Fonte: `CLAUDE.md` §2, §5, §8.
Implementação em `bot/` (`n8n_orion_flow.json`, `README.md`, `env.example`).

## Quando usar
- Ao montar, editar ou operar o fluxo de automação da cadência (Fase 2).

## Stack (self-hosted, VPS do Edmar)
- **n8n** — orquestração (schedule + lógica).
- **Evolution API** — WhatsApp.
- **SMTP/Gmail** — e-mail.
- **Postgres** — estado, fila de revisão, opt-out, logging.
- **Entrada:** `data/escolas_sc_sp.csv` (ou tabela `escolas`).
- Direct do Instagram **fora** do envio automático (só aquecimento manual).

## Comportamento obrigatório
- Roda **somente seg–sex**, janela comercial (09h–18h, America/Sao_Paulo).
- **E-mail:** monta rascunho personalizado e deixa em fila "revisar" → **humano aprova**
  (ou envia só para lista pré-aprovada). Nunca envia frio sem aprovação.
- **WhatsApp:** só para escola com **conversa institucional já aberta**; respeita janela 24h;
  cadência máx. **2 toques** sem resposta → pausa.
- **Follow-up D4/D7/D14** automático conforme Fase 2, lendo `status` de cada escola.
- **Opt-out:** palavra-chave ("sair", "não tenho interesse") → marca `opt-out`, bloqueia **60 dias**.
- **Logging:** cada ação grava em Postgres + atualiza `status`.
- **Rate limit** conservador para preservar o número.

## Cadência (Fase 2, resumo)
D0 ligação+e-mail · D1 IG (humano) · D4 ligação+WhatsApp · D7 e-mail prova social ·
D10 fechamento · D14 último toque. Sem resposta → `descartado`, reciclar em 60d.

## GUARDRAILS (inegociáveis — `CLAUDE.md` §2)
- Sem disparo frio em massa no WhatsApp (viola ToS, queima número).
- Direct: Meta não permite DM fria — só resposta dentro de 24h.
- E-mail frio com moderação, opt-out visível, remetente real (Edmar), **aprovação humana**.
- Primeiro toque frio = **ligação humana** (passo 1), não automação.
