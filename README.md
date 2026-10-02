# Orion Planetários — Operação de Prospecção (SC & SP)

Sistema de prospecção do **Edmar Santos — Representante Oficial da Orion Planetários**.
Meta: **1 escola fechada/semana** em SC e SP (funil 20 → 5 → 2 → 1).

> Fonte da verdade comercial: [`CLAUDE.md`](./CLAUDE.md) (ficha congelada + guardrails LGPD).
> Fonte da verdade operacional (escolas/contatos/status): **Notion** — Hub do Representante.

## Onde vive cada coisa

| Camada | Lugar | Papel |
|---|---|---|
| **Escolas, contatos, status, follow-up** | **Notion** — `Banco de Escolas — SC/SP (DB)` | CRM vivo (humano + bot escrevem). Dados pessoais ficam SÓ aqui (LGPD). |
| Ficha comercial + guardrails | `CLAUDE.md` (este repo) | Regras invioláveis de compliance |
| Mídia do kit (vídeos, fotos, PDFs) | `drive-download-*/` (local) + Google Drive | Biblioteca de criativos (não versionada) |
| Schema + export sanitizado | `data/` (este repo) | Definição do banco + seed sem dado pessoal |
| Apresentação / criativos | `docs/` | PDF "como funciona" + prompts de criativos |
| Bot multicanal | `bot/` | n8n + Evolution API + SMTP + Postgres (Fase 5) |

## Estrutura

```
CLAUDE.md                     # PROMPT_MASTER (fonte da verdade)
data/
  escolas_schema.md           # definição do banco de escolas (espelha o Notion DB)
  escolas_sc_sp.sample.csv    # seed institucional (SEM dado pessoal)
docs/
  apresentacao_orion.html     # PDF de apresentação (abrir no navegador -> Imprimir -> Salvar PDF)
  prompt_criativos_claude_design_canva.md   # prompt pronto p/ criativos
skills/                       # orion-school-mapper / copy-engine / canva-prompts / outreach-bot
bot/                          # fluxo n8n (Fase 5)
```

## Status (02/10/2026)
- [x] Banco de Escolas virou **banco de dados no Notion** + semeado (~96 colégios SC+SP)
- [x] Hub corrigido p/ compliance (OBA, medidas, escassez, foco geográfico)
- [x] Apresentação PDF + prompt de criativos
- [ ] Enriquecer escolas (matrículas/INEP/contato institucional)
- [ ] Bot n8n (Fase 5)

## Compliance (resumo — ver CLAUDE.md §2)
LGPD: só dados institucionais públicos. WhatsApp só após abertura. E-mail com opt-out + aprovação humana. Sem escassez falsa. Opt-out bloqueia 60 dias.
