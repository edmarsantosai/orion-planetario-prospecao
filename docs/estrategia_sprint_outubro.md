# Estratégia Sprint — 10 escolas até 31/out/2026 (SC · SP · PR)

> Meta do Edmar: **10 escolas abertas (data fechada) ainda em outubro**, particulares + públicas.
> Base consolidada: `data/escolas_master.csv` = **208 escolas** (SC 53 · SP 120 · PR 35).
> Duas frentes em paralelo: **automação** (e-mail P1 via Make) + **manual** (telefone, redes, e-mail).
> Hoje = seg 13/out (o dia 12 foi feriado). Janela útil restante: **~13 dias úteis**.

---

## 1. Diagnóstico honesto (leia antes de tudo)

A meta é **~10× o ritmo normal** do funil congelado (1 fechamento/semana = 20→5→2→1). Para 10 fechamentos pela via "1 a 1" seriam necessários, grosso modo, **~200 prospecções → 50 conversas → 20 propostas → 10 fechamentos** — inviável para um operador solo em 13 dias úteis de ligação fria.

**Veredito:** 10 contratos *assinados com data* até 31/out é uma **meta-esticada**. Pela via individual, o resultado realista de altíssimo esforço é **3–4 fechados + pipeline carregado**. O que torna os **10 possíveis** é **não vender 1 a 1**: apostar em **negócios de lote** (1 "sim" que abre várias escolas) e começar pelos **quentes/reativação** (quem já teve planetário fecha mais rápido).

**Portanto a estratégia é 70% lote + 30% blitz individual nos quentes.**

### Armadilhas de calendário (outubro)
- **Qua 15/out = Dia do Professor** — muitas escolas em recesso/meio período. **Não agende ligações-chave nesse dia.**
- **Ter 28/out = Dia do Servidor Público** — redes públicas podem fechar. Priorize públicas antes/depois.

---

## 2. As 3 apostas de LOTE (onde moram os 10) — prioridade máxima

Cada "sim" aqui vale **várias escolas de uma vez**. É aqui que você ataca primeiro, de manhã, com ligação.

### Aposta 1 — Rede SESI-SP (41 unidades na base, e-mails `@sesisp.org.br`)
Decisão tende a ser **regional/central**. Um roteiro itinerante aprovado = **múltiplas unidades** no mesmo "sim".
- Ação: ligar para 2-3 unidades quentes (SP079 Amoreiras, SP099 Ribeirão, SP107 SJCampos) e **pedir o contato da gerência regional/educação**. Script C2 do `roteiro_ligacao_e_canais.md`.
- Potencial: 3–5 escolas de um roteiro só.

### Aposta 2 — Secretarias/NRE (efeito multiplicador público)
1 aprovação de SME/NRE → portfólio na intranet de dezenas de escolas → pilota 2-3 já.
- SC: Secretarias de **Joinville, Blumenau, Itajaí, Içara** (Içara já teve Urânia — porta aberta).
- PR: contatos NRE/SME em `data/_LGPD_pr_nominal.md` (Londrina/Maringá já usaram planetário).
- Script C1. Potencial: 2–4 escolas-piloto rápidas + pipeline enorme.

### Aposta 3 — Redes privadas confessionais/grupos (Bom Jesus, Marista, Adventista, Positivo, Objetivo, Anglo)
Decisor pedagógico regional → **roteiro multi-unidade**. Começar pela unidade mais quente como caso.
- SC: Bom Jesus (R15/R16/R17/R18), Marista (R24/R25), Salesiano (R26).
- SP: Objetivo (SP033/SP069), Anglo (SP063/SP075), Adventista (SP004).
- PR: Positivo (PR01/PR02/PR05), Marista (PR07/PR08/PR09), Adventista (PR03/PR11), Bom Jesus (PR12/PR13).
- Script C3. Potencial: 2–3 escolas por rede que avançar.

---

## 3. Blitz individual nos QUENTES (frente manual, paralela)

### Tier 1 — Reativação (já tiveram planetário → ciclo curto) · LIGAR PRIMEIRO
`R31` EMEF Lúcia De Lucca/Içara · `R32` EB Gaspar da Costa Moraes/Itajaí · `R33` EM Virgínia Soares/Joinville · `R34` EM Padre Valente Simioni/Joinville · `SP113` Madre Cabrini/SP · `SP114` Abaco/SBC · `SP115` Exato/SP · `SP116` EM Maria Luiza/Ibaté · `PR24` América Sabino/Londrina · `PR26` Aristeu Ribas/Londrina · `PR27` Dom Jaime/Maringá.
> Abordagem: *"vocês já viveram a experiência — a nossa é 360° em VR, por faixa etária e BNCC, e sem custo pra escola."*

### Tier 2 — P1 privada quente com telefone+e-mail · BLITZ DE LIGAÇÃO
SC: `R01` Colégio Visão · `R14` Catarinense · `R22` Santa Catarina · `R24` Marista SJ · `R26` Salesiano Itajaí · `R29` Menino Jesus · `R30` CNEC.
SP: `SP001` Notre Dame · `SP002` Photon · `SP032` Porto Seguro Valinhos · `SP044` Santa Maria · `SP039` Sphere · `SP040` **Escola Planetário** (aderência temática!) · `SP045` AZ Internacional · `SP031` Progresso.

### Tier 3 — resto P1/P2 → automação (e-mail P1 via Make) + follow-up
As 48 da `campanha_p1` já estão na planilha do Make; o resto entra na cadência conforme avançam.

---

## 4. Plano diário (2 semanas)

**Toda manhã (09h–12h) = LIGAÇÃO (frente manual):**
- 2h nas **apostas de lote** (SESI / Secretaria / rede). É o que entrega os 10.
- 1h no **Tier 1/2** (quentes e reativação).
- Meta: **15–20 ligações/dia** → registrar tudo no Notion.

**Toda tarde (14h–18h):**
- Aprovar e disparar **e-mail P1 pelo Make** (rampa 5/10/15/20) — ver `bot/make_campanha_p1.md`.
- Reuniões de 15 min agendadas (fechamento).
- Aquecimento manual no Instagram das escolas-alvo do dia.
- Follow-up D4/D7 por e-mail/WhatsApp (canais já abertos).

**Semana 1 (13–17/out):** disparar lotes + blitz Tier 1/2. Meta: **2 fechados + 1 aposta de lote em negociação**.
**Semana 2 (20–24/out):** fechar os lotes + propostas da semana 1. Meta: **+5 a +8 escolas** (vindas de 1-2 lotes).
**Semana 3 (27–31/out):** fechamento final + encaixe de datas em novembro para o excedente.

---

## 5. Funil-alvo do mês (acompanhar no Notion)

| Métrica | Meta mês | Como ler no Notion |
|---|---|---|
| Prospecções (ligações feitas) | ~150 | status `novo`→`contatado` |
| Conversas reais | ~30 | status `conversa` |
| Propostas | ~18 | status `proposta` |
| **Fechamentos** | **10** (esticada) / 4 (base) | status `fechado` |
| Lotes em negociação | **≥2** (SESI + 1 Secretaria/rede) | tag/observação |

> Se no fim da semana 1 **nenhum lote avançou**, recalibre a meta para **4 fechados** e trate os 10 como "escolas quentes no pipe" — honesto com o Edmar e com a Orion.

---

## 6. Compliance (não negociável — CLAUDE.md §2)
- 1º toque frio = **ligação humana**; e-mail automático só na lista P1 pré-aprovada; WhatsApp só em canal já aberto; Direct só aquecimento.
- Opt-out ("sair") encerra a escola por **60 dias**.
- Nomes de decisores (incl. PR) **só no Notion**.
- Sem escassez falsa; OBA não entra em material automatizado até validação escrita da Orion.

---

### Ordem de execução agora
1. **Importar `data/escolas_master.csv` no Notion** (208 escolas) + anexar nominal PR (`_LGPD_pr_nominal.md`).
2. **Ligar as apostas de lote** (SESI / Secretaria / rede) — manhã de hoje.
3. **Ligar Tier 1 (reativação)** — ciclo curto.
4. **Ligar o Make** (e-mail P1) à tarde — ver `bot/make_campanha_p1.md`.
