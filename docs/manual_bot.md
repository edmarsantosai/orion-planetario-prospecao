# Manual de Funcionalidade — Bot de Prospecção Orion

> Operação multicanal (e-mail + WhatsApp) que roda **sozinha de seg a sex, 9h–18h**,
> seguindo a cadência de 14 dias do plano de prospecção. Este manual explica o que o
> bot faz, como ligar/desligar, como operar no dia a dia e como manter a compliance.
>
> **Última atualização:** 2026-10-08 · **Workflow n8n:** `orionmulticanal1` ("Orion — Prospecção Multicanal (seg-sex)")

---

## 0. Quickstart — como disparar os e-mails (passo a passo)

**Os e-mails são disparados sozinhos?** Hoje **não**. Por padrão o bot roda em **modo rascunho**
(todo e-mail vai para a fila de revisão) e, além disso, nenhuma escola está "ligada" ainda.
Para colocar a máquina para rodar com os melhores resultados, siga a ordem:

**Horário da automação:** de hora em hora, **9h às 18h, seg–sex** (fuso São Paulo). Cron `0 9-18 * * 1-5`.
➡️ **Recomendado:** mudar para **1×/dia às 9h** + trava anti-reenvio (ver §6.4) antes de ligar o `auto`.

| Passo | O que fazer | Onde | Obrigatório p/ enviar? |
|---|---|---|---|
| 1 | **Ativar o workflow** (toggle Active) | n8n UI | ✅ |
| 2 | **Definir `data_d0`** nas escolas que quer trabalhar | SQL (§5) | ✅ (sem isso nada sai) |
| 3 | **Revisar/enviar os rascunhos** da fila | SQL `fila_revisar` (§6.3) | ✅ enquanto estiver em rascunho |
| 4 | **(Opcional) Aprovar escolas** `aprovado=true` | SQL (§6.1) | só p/ modo auto |
| 5 | **(Opcional) Ligar modo `auto`** + trava anti-reenvio | nó "Pode enviar auto?" (§6.2/§6.4) | só p/ 100% automático |
| 6 | **Conectar WhatsApp** (QR da instância `orion`) | Evolution (§7) | só p/ o toque D4 |

**Resumo das duas formas de operar:**
- **Semiautomático (recomendado p/ começar):** passos 1–3. O bot monta tudo, você dá o OK e dispara.
  Zero risco de erro de volume, máxima qualidade.
- **Automático total:** passos 1–6. O bot envia sozinho **só para escolas pré-aprovadas**,
  1×/dia, sem repetir toque. Use depois de validar os primeiros lotes.

> **Boas práticas para resultados (e para não queimar o remetente):**
> - Comece com **lotes pequenos** (10–20 escolas/dia), não a base inteira.
> - Rode a cadência **1×/dia** (não de hora em hora) — ver §6.4.
> - Personalize o máximo possível (`nome_coordenacao`, `cidade` já entram no corpo).
> - Monitore a fila e os `eventos` nos primeiros dias antes de soltar o `auto`.
> - Mantenha SPF/DKIM válidos (já estão) e o opt-out no rodapé (já está).

---

## 1. Visão geral — o que o bot faz

O bot automatiza o **reforço** e o **follow-up** da prospecção (o primeiro toque frio continua sendo **ligação humana**, conforme o plano). A cada hora, em dia útil, ele:

1. Busca no banco as escolas "devidas" (que têm data de início e não estão bloqueadas).
2. Calcula em que **etapa da cadência** cada escola está (D0, D4, D7, D14).
3. Dispara o toque do canal certo (e-mail ou WhatsApp) **respeitando os gates de compliance**.
4. Registra tudo (`eventos`) e, quando não pode enviar sozinho, deixa um **rascunho na fila de revisão**.
5. Processa **opt-out** automaticamente (bloqueia a escola por 60 dias).

**Princípio-chave:** por padrão o bot **não envia e-mail sozinho** — ele monta o rascunho e põe
na fila `fila_revisar` para um humano aprovar. O envio automático só acontece para escolas
explicitamente liberadas (`aprovado = true`) **e** com o modo `auto` ligado.

---

## 2. Arquitetura e acessos

| Componente | Onde | Para quê |
|---|---|---|
| **n8n** | https://n8n.edmarsantos.com.br | Orquestração (o workflow `orionmulticanal1`) |
| **Evolution API** | https://api.edmarsantos.com.br | Envio/recebimento de WhatsApp (instância `orion`) |
| **Postgres** (banco `orion`) | container `postgres` na VPS | Estado das escolas, logs, opt-out, fila de revisão |
| **SMTP HostGator** | `srv252.prodns.com.br:465` (SSL) | E-mail, remetente `comercial@edmarsantos.com.br` |

> ⚠️ **Host SMTP:** use `srv252.prodns.com.br` (não `mail.edmarsantos.com.br`). O cert do
> HostGator é `*.prodns.com.br`; com `mail.edmarsantos.com.br` a validação TLS falha e o n8n
> recusa o envio. Testado OK (código 250). Se a HostGator migrar o servidor, confirme o novo
> hostname (`openssl s_client -connect mail.edmarsantos.com.br:465` → reverse DNS do IP).

Acesso ao servidor: `ssh vps-edmar` (stack em produção, **compartilhada com outros projetos** —
cuidado ao reiniciar containers).

**Credenciais no n8n:** `Orion Postgres` (`orion-pg`) e `Orion SMTP HostGator` (`orion-smtp`).

---

## 3. A cadência de 14 dias (o coração do bot)

O bot age com base na coluna `data_d0` de cada escola (a data em que a cadência começou).
A partir dela, conta os dias e decide o toque:

| Dia | Etapa | Canal | O que envia |
|---|---|---|---|
| D0 | `D0` | E-mail | Apresentação + proposta (modelo custo-zero, 10%, telescópio) + PDF anexo |
| D4 | `D4` | WhatsApp | Reforço do convite de reunião (**só se já houver conversa aberta**) |
| D7 | `D7` | E-mail | Follow-up com prova social ("o que as escolas falam depois do planetário") |
| D14 | `D14` | E-mail | Último toque |

> Fora desses dias exatos (D0/D4/D7/D14) o bot não faz nada para aquela escola. Ligações
> (D0/D4/D10) continuam **humanas** e não são feitas pelo bot.

---

## 4. Ligar e desligar o bot

O workflow já está **importado e marcado como ativo** (`orionmulticanal1`).

**Para ativar/desativar ao vivo** (recomendado, sem downtime):
- Abra https://n8n.edmarsantos.com.br → workflow **"Orion — Prospecção Multicanal (seg-sex)"**
- Use o **toggle Active** no topo direito.

> ⚠️ A ativação via linha de comando (`update:workflow --active`) grava no banco mas **só passa
> a valer após o n8n recarregar**. Como o n8n é compartilhado, **não reinicie o container** só
> para isso — use o toggle na UI, que registra o gatilho de agenda na hora.

**Verdade importante:** mesmo ativo, **o bot não envia nada** enquanto nenhuma escola tiver
`data_d0` definida. Esse é o estado seguro atual (175 escolas, 0 com D0).

---

## 5. Operação diária — como colocar uma escola na esteira

### 5.1 Iniciar a cadência de uma escola (definir D0)
Depois da ligação humana (passo 1), para o bot começar a trabalhar aquela escola:

```sql
-- conecte: ssh vps-edmar "docker exec -it postgres psql -U postgres -d orion"
UPDATE escolas SET data_d0 = CURRENT_DATE, status = 'contatado'
WHERE id = 'ID_DA_ESCOLA';
```

A partir daí o bot envia o D0 **naquele dia** (ou cai na fila de revisão — ver §6).

### 5.2 Iniciar um lote (ex.: as 10 escolas P1 de Florianópolis)
```sql
UPDATE escolas SET data_d0 = CURRENT_DATE, status = 'contatado'
WHERE prioridade = 'P1' AND cidade = 'Florianópolis' AND data_d0 IS NULL
LIMIT 10;
```

### 5.3 Ver em que etapa cada escola está hoje
```sql
SELECT nome_escola, cidade, data_d0, CURRENT_DATE - data_d0 AS dias, status
FROM escolas WHERE data_d0 IS NOT NULL ORDER BY data_d0;
```

---

## 6. Modo seguro: rascunho × envio automático

O e-mail passa por um nó **"Pode enviar auto?"** com dois caminhos:

- **Rascunho (padrão):** o e-mail vai para a tabela `fila_revisar` com `status='revisar'`.
  Nada é enviado sem um humano aprovar.
- **Automático:** só dispara se **(a)** o modo estiver em `auto` **e** **(b)** a escola tiver
  `aprovado = true`.

### 6.1 Aprovar escolas para envio automático
```sql
UPDATE escolas SET aprovado = true WHERE id IN ('ESC1','ESC2','ESC3');
```

### 6.2 Ligar o modo automático (quando quiser deixar 100% no automático)
No nó **"Pode enviar auto?"** do workflow, a primeira condição compara o literal `'modo'`
com `'auto'` — como são diferentes, **tudo cai em rascunho por padrão**. Para liberar o
automático-por-lote, edite esse nó e troque o literal `modo` por `auto`, mantendo
`aprovado = true` só nas escolas liberadas.

> **Recomendação:** comece em rascunho, valide os primeiros envios na fila, e só então
> ligue o automático para um lote pequeno e pré-aprovado. Nunca é blast para todos.

### 6.3 Revisar e enviar os rascunhos
```sql
-- ver fila
SELECT id, escola_id, assunto, status, ts FROM fila_revisar WHERE status='revisar' ORDER BY ts;
-- aprovar um rascunho (o envio do item aprovado é feito pelo operador/segundo fluxo)
UPDATE fila_revisar SET status='aprovado' WHERE id = 123;
```

### 6.4 ⚠️ Antes de ligar o `auto`: trava anti-reenvio (idempotência)

O gatilho roda **de hora em hora** (9h–18h). Como o nó "Decidir toque" calcula a etapa pela
diferença de dias, uma escola em D0 seria reprocessada **a cada hora do mesmo dia** — ou seja,
no modo `auto` ela receberia o mesmo e-mail várias vezes no dia. Para resultados corretos,
faça **uma das duas** correções (ou as duas) antes de ligar o automático:

**Opção A — rodar 1×/dia (mais simples).** No nó **"Agenda seg-sex 09-18"**, troque o cron
`0 9-18 * * 1-5` por `0 9 * * 1-5` (só às 9h). Cada toque passa a ser avaliado uma vez por dia.

**Opção B — deduplicar por `eventos` (mais robusta).** No nó **"Buscar escolas devidas"**,
troque a query para excluir escolas que já receberam um toque hoje:

```sql
SELECT e.* FROM escolas e
LEFT JOIN optout o ON o.escola_id = e.id
WHERE e.status NOT IN ('fechado','descartado','opt-out')
  AND (o.bloqueado_ate IS NULL OR o.bloqueado_ate < CURRENT_DATE)
  AND e.data_d0 IS NOT NULL
  AND e.email_institucional IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM eventos ev
    WHERE ev.escola_id = e.id AND ev.acao = 'disparo' AND ev.ts::date = CURRENT_DATE
  );
```

> Recomendação: aplique **A + B** juntas. Assim, mesmo que a agenda rode mais de uma vez,
> nenhuma escola recebe o mesmo toque duas vezes no dia.

---

## 7. WhatsApp — regras e conexão

- Instância **`orion`** na Evolution API (https://api.edmarsantos.com.br).
- **Conectar o número:** na Evolution, gere o QR Code da instância `orion` e escaneie com o
  WhatsApp comercial. (Verifique o status da instância antes de operar.)
- **Gate de compliance (automático no fluxo):** o WhatsApp só dispara se a escola tiver
  `wa_conversa_aberta = true`, menos de 2 toques (`wa_toques < 2`) e dentro da janela de 24h
  do último inbound (`wa_ultimo_inbound`). Sem isso, o bot **pausa** — nunca manda cold.

Quando uma escola responde no WhatsApp institucional, marque:
```sql
UPDATE escolas SET wa_conversa_aberta = true, wa_ultimo_inbound = now(), wa_toques = 0
WHERE id = 'ID_DA_ESCOLA';
```

---

## 8. Opt-out (descadastro)

- Há um **webhook** (`/webhook/orion-optout`) que recebe mensagens inbound.
- Se o texto contém `sair`, `não tenho interesse`, `descadastrar` ou `remover`, o bot:
  - insere/atualiza a escola em `optout` com `bloqueado_ate = hoje + 60 dias`;
  - marca `escolas.status = 'opt-out'`.
- Escolas bloqueadas **não entram** na busca de toques enquanto `bloqueado_ate` for futuro.

Conferir bloqueios ativos:
```sql
SELECT escola_id, motivo, bloqueado_ate FROM optout WHERE bloqueado_ate >= CURRENT_DATE;
```

---

## 9. Monitoramento

Todo disparo é logado em `eventos`:
```sql
-- últimos 20 eventos
SELECT ts, escola_id, canal, etapa, acao, detalhe FROM eventos ORDER BY ts DESC LIMIT 20;
-- resumo por dia
SELECT ts::date AS dia, canal, count(*) FROM eventos GROUP BY 1,2 ORDER BY 1 DESC;
```

No n8n, a aba **Executions** do workflow mostra cada rodada (sucesso/erro) de hora em hora.

---

## 9.1 Entregabilidade — por que um e-mail pode "não chegar"

Um envio pode ser **aceito pelo servidor (código 250)** e ainda assim não aparecer na caixa de
entrada do destinatário. Isso é **filtragem no destino**, não falha do bot. Checklist:

- **DNS do domínio (já OK):** SPF `v=spf1 +mx +a +ip4:162.241.3.31 ~all`, DKIM selector `default`
  publicado, DMARC `p=none`. O IP de envio está autorizado.
- **Onde procurar:** Spam/Promoções. No Gmail, busque `from:comercial@edmarsantos.com.br`
  (varre Todos os e-mails + Spam). Marcar "Não é spam" treina a reputação.
- **Domínio novo = baixa reputação:** os primeiros envios tendem a cair em Spam. **Warm-up:**
  comece com poucos e-mails/dia e aumente gradualmente; peça aos primeiros contatos para
  responderem/marcarem como "não spam".
- **Sem bounce = não foi rejeitado:** bounces chegam em `comercial@edmarsantos.com.br`. Conferir
  essa caixa (IMAP `srv252.prodns.com.br:993`) diz se algo foi recusado.
- **Teste de score:** envie um e-mail para um endereço do **mail-tester.com** para receber uma
  nota 0–10 com os motivos exatos (SPF/DKIM/DMARC/conteúdo).
- **Conteúdo:** evite texto "cara de spam"; o template real já tem estrutura boa, remetente real
  e opt-out no rodapé (ajuda na entrega).

---

## 10. Compliance (não negociável)

- E-mail: opt-out visível no rodapé, remetente real (Edmar), **humano aprova** por padrão.
- WhatsApp: **nunca** cold; só conversa institucional já aberta, janela 24h, máx. 2 toques.
- LGPD: só dados de canais institucionais públicos; nomes de decisores ficam **fora do Git**.
- Opt-out encerra a escola por **60 dias**.
- Sazonalidade e decisor (coordenação/direção) seguem o `CLAUDE.md` e o `plano_prospeccao.md`.

---

## 11. Manutenção e pendências

- **Senha SMTP:** foi definida via chat; por segurança, **troque no cPanel** e atualize só na
  credencial `orion-smtp` do n8n. Envio de teste validado (código 250) em 2026-10-08.
- **Host SMTP = `srv252.prodns.com.br`** (não `mail.edmarsantos.com.br` — cert mismatch).
- **Conectar/validar a instância `orion`** no WhatsApp (QR) antes do primeiro D4.
- **Aviso do n8n:** "Postgres 15 is not supported" — é só *warning* de compatibilidade; o bot
  funciona. Planejar upgrade do Postgres como manutenção futura (afeta a stack inteira).
- **Enriquecer base:** matrículas/INEP e novos lotes conforme a Fase 1.

---

## 12. Troubleshooting rápido

| Sintoma | Causa provável | Ação |
|---|---|---|
| Bot ativo mas não envia nada | Nenhuma escola com `data_d0` | Definir `data_d0` (§5) |
| E-mail não sai, vai pra fila | Modo em rascunho (padrão) | Normal; aprove na fila ou ligue auto (§6) |
| E-mail dá erro de autenticação | Senha SMTP errada na credencial | Reconferir `orion-smtp` no n8n |
| WhatsApp não dispara | Sem conversa aberta / fora da janela 24h | Esperar inbound; marcar `wa_conversa_aberta` (§7) |
| Escola sumiu dos toques | Entrou em opt-out | Ver `optout` (§8); volta após 60 dias |
| Gatilho de agenda não roda | Workflow não recarregou após ativar via CLI | Usar o toggle Active na UI (§4) |
