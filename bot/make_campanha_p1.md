# Make.com — Campanha de e-mail P1 (provisório, VPS fora)

> Substitui o fluxo n8n enquanto a VPS está fora do ar. Envia o e-mail HTML
> `docs/apresentacao_email.html` para as 48 escolas P1 de `data/campanha_p1.csv`,
> com rampa de aquecimento, personalização, anti-reenvio e cabeçalhos corretos.
>
> **SMTP é independente da VPS** (`srv252.prodns.com.br` é o mail da HostGator/prodns),
> por isso o envio funciona mesmo com a VPS caída.

---

## Parâmetros congelados (fonte: memória `orion-campanha-out2026`)

| Campo | Valor |
|---|---|
| SMTP host | `srv252.prodns.com.br` |
| SMTP porta | `465` (SSL/TLS) |
| Usuário / From | `comercial@edmarsantos.com.br` |
| From (nome) | `Edmar Santos — Orion Planetários` |
| Reply-To | `edmar.orionplanetarios@gmail.com` |
| BCC (2) | `edmarsantos.unasp@gmail.com`, `edmar.orionplanetarios@gmail.com` |
| Corpo | HTML de `docs/apresentacao_email.html` |
| Placeholders | `{{NOME_COORDENACAO}}`, `{{NOME_ESCOLA}}`, `{{CIDADE}}` |
| Janela | ter 13/out → sex 16/out, 09:00 e 14:00 (America/Sao_Paulo) |
| Rampa (por lote) | 13→5, 14→10, 15→15, 16→20 (×2 lotes/dia = 10/20/30/40) |
| Anti-reenvio | coluna `enviado` (marca data/hora após envio) |

Colunas da planilha (ordem do CSV): `A=id  B=uf  C=cidade  D=nome_escola  E=email_institucional  F=nome_coordenacao  G=enviado`

---

## AS 3 AÇÕES QUE SÃO SÓ SUAS (o resto já vem pronto)

1. **Subir a base pro Google Sheets.** Crie uma planilha nova no Drive do
   `edmarsantos.unasp@gmail.com`, `Arquivo → Importar → Upload` e selecione
   `data/campanha_p1.csv` (manter a 1ª linha como cabeçalho). Nome sugerido:
   **`Orion Campanha P1`**, aba **`Página1`**.
2. **Autorizar 2 conexões no Make** (uma vez cada):
   - **Email (SMTP)** → host/porta/usuário acima + a **senha** do `comercial@`.
   - **Google Sheets** → login com `edmarsantos.unasp@gmail.com`.
3. **Ligar o cenário** (toggle ON) depois de conferir o agendamento. Ligar = sua
   aprovação de envio (guardrail da CLAUDE.md: envio só para lista pré-aprovada — a P1).

Tudo abaixo (lógica de rampa, personalização, cabeçalhos, anti-reenvio, agenda) já está no blueprint.

---

## Importar o cenário

No Make: **Scenarios → Create a new scenario → (menu “…”) → Import Blueprint** e cole o JSON
abaixo. Depois do import, 3 módulos vão pedir pra escolher a **conexão** (SMTP e Google Sheets)
e a **planilha/aba** — selecione a planilha do passo 1.

> ⚠️ **4 campos a conferir após importar** (variações de versão de módulo do Make):
> 1. No **Search Rows** e **Update a Row**: selecionar Spreadsheet = `Orion Campanha P1`, Sheet = `Página1`.
> 2. **“Table contains headers” = Yes** nos dois módulos de planilha.
> 3. No **Update a Row**, o campo **Row number** deve mapear `{{2.__ROW_NUMBER__}}` (número da linha vindo do Search).
> 4. Confirme que o **filtro** do Search Rows é “coluna G (`enviado`) **Is empty**”.

```json
{
  "name": "Orion — Campanha P1 (provisório Make)",
  "flow": [
    {
      "id": 2,
      "module": "google-sheets:searchRows",
      "version": 2,
      "parameters": {},
      "mapper": {
        "from": "drive",
        "mode": "select",
        "includesHeaders": true,
        "limit": "{{switch(formatDate(now; \"D\"; \"America/Sao_Paulo\"); \"13\"; 5; \"14\"; 10; \"15\"; 15; \"16\"; 20; 0)}}",
        "sortOrder": "asc",
        "filter": [
          [
            { "a": "G", "b": "", "o": "text:empty" }
          ]
        ]
      },
      "metadata": {
        "designer": { "x": 0, "y": 0 },
        "restore": {},
        "parameters": []
      }
    },
    {
      "id": 3,
      "module": "email:ActionSendEmail",
      "version": 5,
      "parameters": {},
      "filter": {
        "name": "tem e-mail",
        "conditions": [
          [
            { "a": "{{2.`E`}}", "o": "exist" }
          ]
        ]
      },
      "mapper": {
        "to": ["{{2.`E`}}"],
        "cc": [],
        "bcc": [
          "edmarsantos.unasp@gmail.com",
          "edmar.orionplanetarios@gmail.com"
        ],
        "replyTo": "edmar.orionplanetarios@gmail.com",
        "from": "comercial@edmarsantos.com.br",
        "sender": "Edmar Santos — Orion Planetários",
        "subject": "Um planetário 360° dentro da {{2.`D`}} — sem custo para a escola",
        "contentType": "html",
        "html": "<!-- COLAR AQUI o HTML de docs/apresentacao_email.html, com os 3 placeholders trocados por: {{NOME_COORDENACAO}} -> {{2.`F`}} ; {{NOME_ESCOLA}} -> {{2.`D`}} ; {{CIDADE}} -> {{2.`C`}} -->",
        "attachments": []
      },
      "metadata": {
        "designer": { "x": 300, "y": 0 },
        "restore": {},
        "parameters": []
      }
    },
    {
      "id": 4,
      "module": "google-sheets:updateRow",
      "version": 2,
      "parameters": {},
      "mapper": {
        "from": "drive",
        "mode": "select",
        "includesHeaders": true,
        "rowNumber": "{{2.`__ROW_NUMBER__`}}",
        "values": {
          "G": "{{formatDate(now; \"YYYY-MM-DD HH:mm\"; \"America/Sao_Paulo\")}}"
        }
      },
      "metadata": {
        "designer": { "x": 600, "y": 0 },
        "restore": {},
        "parameters": []
      }
    }
  ],
  "metadata": {
    "instant": false,
    "version": 1,
    "scenario": {
      "roundtrips": 1,
      "maxErrors": 3,
      "autoCommit": true,
      "autoCommitTriggerLast": true,
      "sequential": true,
      "slots": null,
      "confidential": false,
      "dataloss": false,
      "dlq": false,
      "freshVariables": false
    },
    "designer": { "orphans": [] },
    "zone": "us2.make.com"
  }
}
```

### Corpo HTML (colar no campo `html` do módulo Email)

Abra `docs/apresentacao_email.html`, copie o conteúdo inteiro e cole no campo **Content / HTML**
do módulo *Send an Email*. Depois troque os 3 placeholders pelos mapeamentos da planilha:

| No HTML | Trocar por (mapeamento Make) |
|---|---|
| `{{NOME_COORDENACAO}}` | `` {{2.`F`}} `` |
| `{{NOME_ESCOLA}}` | `` {{2.`D`}} `` |
| `{{CIDADE}}` | `` {{2.`C`}} `` |

(São os únicos 3 pontos de personalização. O resto do HTML é fixo.)

---

## Agendamento (2 lotes/dia, ter–sex)

Na engrenagem de **Scheduling** do cenário, use **Advanced scheduling** e adicione **2 itens**:

| Item | Tipo | Dias | Hora |
|---|---|---|---|
| Lote manhã | Days of the week | Tue, Wed, Thu, Fri | 09:00 |
| Lote tarde | Days of the week | Tue, Wed, Thu, Fri | 14:00 |

Fuso do cenário: **America/Sao_Paulo** (Organization/Scenario settings).

**Como a rampa funciona sozinha:** o `limit` do Search Rows é calculado pela data
(`13→5, 14→10, 15→15, 16→20`); cada lote envia esse nº → 5+5, 10+10, 15+15, 20+20.
Fora de 13–16/out o `limit` é `0` → não envia nada (seguro deixar ligado).

**Anti-reenvio:** o Search só pega linhas com `enviado` vazio; o Update marca a data/hora
após enviar. Reexecuções nunca repetem uma escola já contactada.

---

## Checklist antes de ligar

- [ ] Planilha `Orion Campanha P1` criada e com as 48 linhas (cabeçalho na linha 1)
- [ ] Conexão SMTP autorizada (teste: enviar 1 e-mail manual pro seu gmail)
- [ ] Conexão Google Sheets autorizada
- [ ] HTML colado + 3 placeholders mapeados
- [ ] Filtro `G Is empty` e Row number `{{2.__ROW_NUMBER__}}` conferidos
- [ ] 2 horários no scheduling (09:00 / 14:00, ter–sex), fuso São Paulo
- [ ] **Run once** com 1–2 linhas de teste (ou `limit` temporário = 1) antes de abrir geral

---

## Observações de compliance (CLAUDE.md §2)

- Opt-out já está no rodapé do HTML (“responda **sair**”). Respostas caem no
  `edmar.orionplanetarios@gmail.com` (Reply-To) — ao receber “sair”, marque a escola e **não
  reenvie por 60 dias** (coluna `enviado` + um `opt-out` manual por enquanto).
- Envio só para **lista pré-aprovada** (P1) = atende ao guardrail de aprovação humana.
- Rampa de aquecimento protege a reputação do domínio novo.
