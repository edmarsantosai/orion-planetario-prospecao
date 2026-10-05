# Plano Executivo de Prospecção — Orion Planetários (SC & SP)

> **Fase 2** do PROMPT_MASTER ([`CLAUDE.md`](../CLAUDE.md)). Fonte da verdade comercial = `CLAUDE.md` §1.
> Fonte da verdade operacional (escolas/status/contatos) = **Notion** `Banco de Escolas — SC/SP (DB)`.
> Todos os disparos obedecem aos **GUARDRAILS §2** (LGPD, WhatsApp, Direct, e-mail, escassez honesta, opt-out).

---

## Diagnóstico

A meta é **1 escola fechada/semana**. O funil que sustenta isso:

```
20 escolas prospectadas  →  5 conversas reais  →  2 propostas  →  1 fechamento   (por semana)
```

Para manter esse ritmo, o pipeline nunca pode esvaziar: **toda segunda-feira entram 20 escolas novas** no topo (status `novo`), enquanto as da semana anterior avançam pela cadência de 14 dias abaixo.

**Dois tempos, dois donos:**

| Dono | O que faz | Por quê |
|---|---|---|
| **Humano (Edmar)** | Todo **primeiro toque frio** (ligação D0, D4, D10) + aquecimento no Instagram | Ligação humana não queima número nem viola ToS; é onde se pega o **nome da coordenação** e se faz a **pergunta de ouro** |
| **Bot (n8n)** | **Reforço e follow-up** (e-mail rascunhado, WhatsApp só em canal já aberto) | Automação entra depois que o humano abriu a porta — nunca antes |

**Regra dura:** o primeiro contato **nunca** é disparo automático. É ligação. O bot só age quando a escola já respondeu ou o número institucional já abriu conversa.

---

## 1. Entrada semanal (topo do funil)

- **Segunda, 09h:** puxar do Notion 20 escolas `novo`, priorizadas (P1 → P2 → P3).
- **Ordem geográfica (campo 30/09):** BC / Itajaí / litoral norte estão **"batidos"** → tratar como **reativação** (não frio). Priorizar frio em **Vale do Itajaí** (Blumenau, Gaspar, Indaial, Timbó) e **Norte** (Joinville, Jaraguá do Sul), depois SP.
- **Decisor-alvo:** coordenação pedagógica **ou** direção. **Nunca fechar com a secretaria** — ela é gatekeeper; o objetivo com ela é só *passar* para o decisor.

---

## 2. Cadência de 14 dias (por escola)

Cada escola percorre esta trilha a partir do D0 (dia da 1ª ligação). O bot lê o campo `status` no Notion para saber qual toque disparar.

| Dia | Canal | Dono | Objetivo | Regra de parada | `status` após |
|---|---|---|---|---|---|
| **D0** | 📞 Ligação | Humano (Edmar) | **Passo 1:** falar com direção/coordenação. **Não vender** — pegar **nome + contato institucional** e fazer a *pergunta de ouro* (abaixo). | Se não passar da secretaria: obter ao menos **1 contato institucional** e agendar retorno | `contatado` |
| **D0** | ✉️ E-mail | Bot (rascunho → Edmar aprova) | Enviar **resumo da proposta** + **vídeo explicativo**. Confirma por escrito o que foi falado na ligação. | Opt-out → encerra (60 dias) | `contatado` |
| **D1** | 📸 Instagram | Humano | **Aquecimento:** seguir o perfil + reagir a 1 story/post recente. Sem DM fria. | — | (mantém) |
| **D4** | 📞 Ligação | Humano | **Passo 2:** falar com a **direção**, quebrar objeções (seção 3), **propor reunião online de 15 min**. | Máx. **3 tentativas**; sem sucesso → segue só por e-mail | `conversa` (se avançou) |
| **D4** | 💬 WhatsApp | Bot (**só se nº institucional já respondeu**) | Reforço do convite de reunião + link do resumo. | Sem resposta em **2 toques** → pausa | `conversa` |
| **D7** | ✉️ E-mail | Bot (rascunho) | **Follow-up com prova social:** depoimentos + vídeo (+200.000 alunos, @orionplanetarios). | Opt-out → encerra | (mantém) |
| **D10** | 📞/💬 Ligação ou WhatsApp | Humano | **Passo 3 — fechamento:** apresentar o **modelo de ingresso** (escola não paga, 10% de repasse, sorteio de telescópio). Diária **só** se rejeitarem o ingresso. | — | `proposta` → `fechado` |
| **D14** | ✉️ E-mail | Bot | **Último toque:** "mantemos seu contato para o próximo semestre?" (soft close, sem pressão). | Sem resposta → `descartado`, reciclar em **60 dias** | `descartado` |

### A pergunta de ouro (toda ligação D0)
> **"Qual planetário vocês já receberam na escola?"**

- Descobre histórico sem depender de dado público (que **não existe** — ver caveat abaixo).
- Expõe o concorrente (nº 1 hoje = **Urânia**) e abre o ângulo de diferenciação Orion (BNCC + VR por faixa etária + modelo custo-zero + sorteio de telescópio).
- Atualiza o campo `Já teve planetário` → `sim | provável | não identificado` (**nunca** marcar `não`).

### Caveat de verificação (LGPD + honestidade)
"Escola não recebeu planetário nos últimos 2 anos" **não é verificável por fonte pública**. Só se **infere** (Instagram da escola, notícia local, registro interno Orion). A confirmação real é **sempre a ligação D0**. Não afirmar "exclusividade na sua cidade" sem base.

---

## 3. Quebra das 7 objeções

Tom **consultivo e humano** (não vendedor agressivo). Cada resposta é curta e **devolve ao CTA** (reunião de 15 min). Variáveis: `{nome_escola}`, `{nome_coordenacao}`, `{cidade}`.

| # | Objeção | Resposta curta (ponte pro CTA) |
|---|---|---|
| 1 | **"Não temos verba / custo"** | "Esse é o melhor da notícia: **a escola não paga nada**. O ingresso é do aluno (ref. R$ 30), a Orion faz toda a divulgação e a escola **ainda recebe 10%** do arrecadado. Posso te mostrar os números numa call de 15 min?" |
| 2 | **"Agenda/calendário cheio"** | "A sessão é **itinerante e flexível** — a gente encaixa num turno só, sem bagunçar o calendário. Encaixa lindo na **Semana Nacional de C&T** ou no planejamento do ano letivo. Qual janela faria sentido pra vocês?" |
| 3 | **"Não temos espaço físico"** | "Precisamos de um **espaço coberto de ~7×6 m, pé-direito 3,2 m e uma tomada 220V** — quadra ou salão já servem. `[VALIDAR COM A ORION: medida exata]` Me conta o que vocês têm que eu confirmo na hora se cabe." |
| 4 | **"Já tivemos planetário"** | "Que ótimo! **Qual vocês receberam?** O nosso é aula de astronomia em **realidade virtual, por faixa etária e alinhada à BNCC** — bem diferente da cúpula passiva. Vale ver a diferença numa call rápida." |
| 5 | **"Preciso falar com a mantenedora/direção"** | "Perfeito, é exatamente com quem a gente adora falar. Posso te mandar um **resumo de 1 página** pra você levar, e a gente faz uma call de 15 min com quem decide? Qual o melhor contato?" |
| 6 | **"E a segurança dos alunos?"** | "Estrutura **inflável certificada**, monitores da Orion acompanham todas as sessões e o fluxo é organizado por turma. Mostro como funciona na prática no vídeo que te envio." |
| 7 | **"Qual a relevância pedagógica?"** | "Conteúdo **alinhado à BNCC (Ciências da Natureza / Astronomia)**, adaptado por faixa etária — vira matéria de sala, não só passeio. E os alunos concorrem a um **telescópio semiprofissional**. Te mostro o plano pedagógico na call?" |

> **OBA:** o claim "única empresa parceira da OBA" **NÃO** entra em material automatizado até a Orion validar por escrito (CLAUDE.md §1). Não usar como argumento de venda ainda.

---

## 4. Regras de disparo, opt-out e reciclagem

- **Janela:** bot roda **seg–sex, 09h–18h** (America/Sao_Paulo). Nada fora disso.
- **E-mail:** o bot **só rascunha** e deixa em fila "revisar"; **Edmar aprova antes de enviar**. Opt-out visível no rodapé + remetente real (Edmar Santos · `edmar.orionplanetarios@gmail.com`).
- **WhatsApp:** disparo **só** para escola com **conversa institucional já aberta**; respeita janela de 24h; **máx. 2 toques sem resposta → pausa**. Remetente: **(47) 99200-9480** (`wa.me/5547992009480`).
- **Instagram Direct:** **só aquecimento** (seguir, reagir, responder story). **Nunca** cold blast — a API da Meta não permite DM fria e automação não-oficial bane o perfil.
- **Opt-out:** palavra-chave ("sair", "não tenho interesse", "descadastrar") → status `opt-out` + **bloqueio de 60 dias**. Qualquer canal.
- **Escassez honesta:** proibido "só restam 2 datas" se não for verdade.
- **Reciclagem:** `descartado` volta ao topo do funil em **60 dias** (reativação, não frio).

---

## 5. Métricas da semana (acompanhar no Notion)

| Métrica | Meta | Onde ler |
|---|---|---|
| Escolas novas prospectadas | 20 | contagem de `novo` → `contatado` na semana |
| Conversas reais | 5 | status `conversa` |
| Propostas enviadas | 2 | status `proposta` |
| Fechamentos | **1** | status `fechado` |
| Opt-outs | monitorar | status `opt-out` |

Se `conversas < 5` numa semana → o gargalo está no **Passo 1 (ligação D0)**: revisar lista P1/P2 e abordagem na secretaria.
Se `propostas < 2` → gargalo no **Passo 2 (quebra de objeções D4)**: revisar seção 3.

---

### Próximo (Fase 3)
`docs/copy_ativos.md` — os ativos de copy A/B por canal que alimentam os toques D0/D4/D7/D14 desta cadência.
