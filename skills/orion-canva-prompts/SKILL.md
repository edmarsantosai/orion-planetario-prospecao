---
name: orion-canva-prompts
description: Use ao gerar prompts de criativos premium (Canva Pro) para a Orion — resumo da proposta, carrossel, reels e contagem regressiva. Define objetivo, formato, paleta, tipografia, copy-base e CTA. Fase 4.
---

# orion-canva-prompts

Como gerar peças premium nível agência para a Orion. Fonte: `CLAUDE.md` §7. Prompts prontos em
`docs/canva_prompts.md`; referências visuais em `docs/criativos/*.png`.

## Quando usar
- Ao produzir ou revisar qualquer criativo (social, e-mail, pós-fechamento).
- Se o MCP do Canva estiver conectado, use `generate-design` / `edit-design` com o briefing.

## Identidade visual (fixa)
- **Paleta:** índigo/violeta (#4B3FA6 / #A98CF2) + dourado (#F5C14E / #E7A82E) + ciano (#29ABE2),
  fundo quase-preto (#02030A).
- **Tipografia:** Sora (display 700–800) + Inter (corpo 400–600).
- **Composição:** full-bleed — foto de fundo + overlay escurecendo (técnica pôster). Texto denso
  sempre sobre área escura. **Sem quadros/círculos/molduras.**
- **Marca:** logo Orion + @orionplanetarios.

## Todo prompt deve especificar
Objetivo · formato/dimensão · paleta · tipografia · copy-base · CTA.

## Peças mínimas (§7)
1. **Resumo da proposta** — 1 página (e-mail/WhatsApp).
2. **Carrossel** "Como funciona o planetário na escola" — 5 cards.
3. **Reels** — capa + roteiro (hook 3s · como funciona 15–25s · CTA).
4. **Contagem regressiva** — 7/5/3/2/1 dia (escola que fechou).

## Ângulos de copy (ver orion-copy-engine)
Custo zero · escola se destaca · BNCC/imersão · 10% de repasse · sorteio de telescópio.

## GUARDRAILS
- **OBA só após validação escrita.** Medidas provisórias "~7×6 m · 3,2 m · 220V".
- Sem escassez falsa. Canais oficiais: @orionplanetarios · orionplanetarios.com.br · Sympla.
- Dado ausente → `[VALIDAR COM A ORION]`.
