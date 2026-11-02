# CRM Orion no NocoDB + fluxo de disparo (runbook)

> **Arquitetura (fonte única da verdade):**
> ```
> NocoDB (crm.edmarsantos.com.br)  →  Postgres `orion`.escolas  ←  n8n (orionmulticanal1)
>    você edita aqui                     MESMA tabela                dispara e-mail/WhatsApp
> ```
> Você edita a escola no NocoDB; o n8n lê o **mesmo** registro na hora. Sem sync, sem reenvio fantasma.
> Notion continua como **hub de material/decisões** — não é o motor.

---

## Parte A — Subir o NocoDB (uma vez)

### A1. DNS (Cloudflare)
Criar registro **A**: `crm` → IP da VPS (`2.25.172.56`). Pode deixar **proxied (nuvem laranja)** — o Traefik usa certresolver `cloudflare` (mesmo padrão do site). Propaga em ~1 min.

### A2. Deploy
```bash
# na VPS, dentro do repo (ou copie a pasta bot/nocodb/)
cp bot/nocodb/.env.example bot/nocodb/.env   # e edite a senha admin
docker compose -f bot/nocodb/docker-compose.yml up -d
docker logs -f nocodb                        # aguarde "App started"
```
> Antes, confirme que a rede do Postgres é mesmo `internal`:
> `docker inspect postgres --format '{{range $k,$v := .NetworkSettings.Networks}}{{$k}} {{end}}'`
> Se vier outro nome, ajuste `networks:` no compose (o `proxy` já está certo).

### A3. 1º login
Abra `https://crm.edmarsantos.com.br` → entre com o `NC_ADMIN_*` do `.env` → **troque a senha**.

---

## Parte B — Conectar a base `orion` (uma vez)

> ⚠️ **Versão do NocoDB importa:** use **0.264.9** (já fixado no compose). As versões **2026.x** têm um guard anti-SSRF que recusa conectar a host privado (`postgres`) com `"Connection to internal hosts is not allowed"` — e **não há env de override**. Conectado e validado via API em 0.264.9 (2026-11-02).

1. **New Base → Connect to external database → PostgreSQL.**
2. Dados de conexão:
   - Host: `postgres`  ·  Port: `5432`  ·  Database: `orion`
   - User: `postgres`  ·  Password: (a do Postgres da stack)
   - SSL: off (rede interna Docker)
3. NocoDB detecta as tabelas `escolas`, `eventos`, `optout`, `fila_revisar`. Abra **`escolas`**.

> ⚠️ **Regra de ouro (Edmar):** só **adicionar/enriquecer**, **NUNCA remover** dados. No NocoDB,
> não use "Delete row" em escolas — para encerrar um contato use `status` = `descartado`/`opt-out`.

---

## Parte C — As 3 views da tabela `escolas`

| View | Tipo | Para quê | Config |
|---|---|---|---|
| **Funil** | **Kanban** | Ver o pipeline | Agrupar por `status` (novo→contatado→conversa→proposta→fechado) |
| **Cadastro** | **Form** | Adicionar escola nova (inclusive do celular) | Campos: `id, uf, cidade, nome_escola, rede, email_institucional, telefone_institucional, instagram, prioridade` |
| **Liberar envio** | **Grid** | Marcar quem o bot pode enviar | Filtro `prioridade = P1` · colunas visíveis: `nome_escola, cidade, email_institucional, aprovado, data_d0, status` |

**Campos e o que significam** (não invente outros — são os de `bot/init.sql`):
- `aprovado` (checkbox) → **true = o n8n pode enviar e-mail automático**. É o freio de mão do modo seguro.
- `data_d0` (data) → início da cadência (D0). Deixe vazio até liberar; preencher dispara a régua D0/D4/D7/D14.
- `wa_conversa_aberta` / `wa_ultimo_inbound` → WhatsApp só entra quando a escola **já respondeu** (janela 24h).
- `status` → estado no funil (nunca apague a linha; mude o status).

**Para liberar uma escola para envio:** na view *Liberar envio*, marque `aprovado` ✅ e preencha `data_d0` com a data do disparo. Só isso.

---

## Parte D — Ajuste do fluxo n8n (corrige o reenvio) ⚠️

O workflow `orionmulticanal1` já lê o Postgres, mas tem **2 pendências** anotadas:

1. **Cron horário → diário.** Hoje `0 9-18 * * 1-5` (reenviaria o mesmo toque toda hora). Trocar para
   **`0 9 * * 1-5`** (uma vez por dia útil, 9h America/Sao_Paulo).
2. **Dedupe por `eventos`.** Antes de enviar, checar se já existe evento do mesmo `(escola_id, etapa)`:
   ```sql
   -- node "dedupe" (Postgres) — só segue quem NÃO tem o toque registrado na etapa
   SELECT e.* FROM escolas e
   LEFT JOIN eventos ev
     ON ev.escola_id = e.id AND ev.etapa = 'D0' AND ev.canal = 'email'
   WHERE e.prioridade = 'P1'
     AND e.aprovado = true
     AND e.status = 'novo'
     AND e.data_d0 = CURRENT_DATE
     AND ev.id IS NULL;          -- ainda não enviou o D0
   ```
3. Após enviar: `INSERT INTO eventos (escola_id,canal,etapa,acao) VALUES ($id,'email','D0','enviado')`
   e `UPDATE escolas SET status='contatado', data_atualizacao=CURRENT_DATE WHERE id=$id`.
4. **Modo seguro mantido:** sem `aprovado=true` + `data_d0` preenchido, **nada sai**.

> E-mail = **HTML no corpo** (`docs/apresentacao_email.html`) + link "ver online"; **sem anexo PDF**
> (anexo frio → spam). PDF só no WhatsApp/follow-up quente.
>
> **Cópia oculta obrigatória em TODO envio (inclusive o 1º):**
> `BCC = edmarsantos.unasp@gmail.com, edmar.orionplanetarios@gmail.com`
> `Reply-To = edmar.orionplanetarios@gmail.com` · `From = comercial@edmarsantos.com.br`.
> No n8n, fixar esses dois endereços no campo **BCC** do node de e-mail (não como variável) para garantir cópia sempre.

---

## Parte E — Desligar o Make (migração concluída)
1. No painel do Make: **pausar/desligar** o cenário de disparo.
2. **Revogar o token da API do Make** (vazou no chat) — Make → Profile → API tokens → revoke.

---

## Rampa de aquecimento (escolas particulares P1)
Começar **terça 03/11** (sexta é dia fraco de B2B): **5 → 10 → 15 → 20** por dia, marcando `aprovado` + `data_d0` em lotes no NocoDB. Antes, 1 e-mail de **teste** (Gmail + Outlook) pra confirmar inbox.
