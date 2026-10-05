---
name: orion-copy-engine
description: Use ao escrever ou revisar copy de prospecção da Orion (e-mail, WhatsApp, Direct, confirmação). Define tom, ângulos que convertem, limites por canal, variáveis e guardrails de compliance. Fase 3.
---

# orion-copy-engine

Regras de copy que convertem no modelo Orion. Fonte de verdade: `CLAUDE.md` §1, §2, §6.
Ativos prontos em `docs/copy_ativos.md`.

## Quando usar
- Ao criar/editar qualquer mensagem de contato ou follow-up.
- Antes de o bot (Fase 5) montar rascunhos.

## Tom
Consultivo, humano, energia alta. **Nunca** vendedor agressivo. Foco no benefício da escola.

## Ângulos que convertem (modelo Orion)
1. **Custo zero** para a escola (aluno paga o ingresso, ref. R$30).
2. **A escola se destaca** / marketing para matrículas.
3. **BNCC + experiência imersiva** 360° por faixa etária.
4. **10% de repasse** para a instituição.
5. **Sorteio de telescópio** semiprofissional.
- OBA ("única empresa do Brasil parceira da OBA") → **só após validação escrita da Orion**.

## Limites por canal
| Canal | Limite | Regra |
|---|---|---|
| E-mail | assunto + corpo ≤ 120 palavras, 1 CTA (reunião online) | opt-out visível no rodapé; bot **rascunha**, humano aprova |
| WhatsApp | 1º contato ≤ 60 palavras + 1 follow-up | **só** canal institucional que já respondeu; janela 24h |
| Direct IG | ≤ 40 palavras | **aquecimento/resposta** — nunca cold blast |
| Confirmação pós-fechamento | — | data, medidas provisórias, ingresso R$30, pagamento na secretaria, 10%, financeiro (Laís) |

## Variáveis
`{nome_escola}` · `{nome_coordenacao}` · `{cidade}` · `{link_resumo}` · `{link_video}`.
Sempre A/B (2 variações por canal).

## Decisor
Coordenação pedagógica ou direção — **nunca** fechar com a secretaria (gatekeeper).

## GUARDRAILS (inegociáveis — `CLAUDE.md` §2)
- Opt-out encerra a escola por **60 dias**.
- Sem escassez falsa ("só restam 2 datas" só se for verdade).
- Medidas físicas provisórias: "~7×6 m · 3,2 m · 220V" (não misturar com 7×8/3,5 do site).
- Remetente real: **Edmar Santos**. Canais: @orionplanetarios · orionplanetarios.com.br · Sympla.
- Dado ausente → `[VALIDAR COM A ORION]`.
