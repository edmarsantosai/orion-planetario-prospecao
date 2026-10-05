# Orion Outreach Bot (Fase 5)

Bot multicanal de prospecção (seg–sex) que executa a cadência da Fase 2 lendo a base de escolas,
**rascunhando e-mails para aprovação humana**, enviando WhatsApp só em conversa já aberta e
registrando tudo em Postgres. Fonte de verdade: [`CLAUDE.md`](../CLAUDE.md) §2, §5, §8.

> **Compliance (inegociável):** o bot **não dispara e-mail frio sem aprovação**. Por padrão
> (`EMAIL_MODO=draft`) ele apenas monta o rascunho e põe na fila `revisar`. Envio automático só
> para escolas marcadas `aprovado=true` (lista pré-aprovada pelo Edmar). WhatsApp só para número
> institucional que já respondeu. Direct do Instagram fica **fora** do envio automático.

## Stack
- **n8n** — orquestração (`bot/n8n_orion_flow.json`)
- **Evolution API** — WhatsApp
- **SMTP/Gmail** — e-mail (remetente real: Edmar)
- **Postgres** — estado, fila de revisão, opt-out, logging
- Entrada: tabela `escolas` (importada de [`../data/escolas_sc_sp.csv`](../data/escolas_sc_sp.csv))

## Setup
1. `cp bot/env.example bot/.env` e preencha (SMTP App Password, Evolution API key, Postgres).
2. Suba os serviços (exemplo `docker-compose.yml` com n8n + postgres + evolution):
   ```bash
   docker compose up -d
   ```
3. Crie o schema no Postgres:
   ```sql
   CREATE TABLE escolas (
     id TEXT PRIMARY KEY, uf TEXT, cidade TEXT, nome_escola TEXT, rede TEXT,
     email_institucional TEXT, telefone_institucional TEXT, instagram TEXT,
     nome_coordenacao TEXT, prioridade TEXT,
     status TEXT DEFAULT 'novo',            -- novo|contatado|conversa|proposta|fechado|descartado|opt-out
     aprovado BOOLEAN DEFAULT false,        -- true = pode enviar e-mail automático
     wa_conversa_aberta BOOLEAN DEFAULT false,
     wa_ultimo_inbound TIMESTAMPTZ,         -- p/ janela 24h
     wa_toques INT DEFAULT 0,
     data_d0 DATE,                          -- início da cadência
     proximo_passo TEXT, data_atualizacao DATE
   );
   CREATE TABLE eventos (
     id BIGSERIAL PRIMARY KEY, escola_id TEXT REFERENCES escolas(id),
     canal TEXT, etapa TEXT, acao TEXT, detalhe TEXT, ts TIMESTAMPTZ DEFAULT now()
   );
   CREATE TABLE optout (
     escola_id TEXT PRIMARY KEY, motivo TEXT,
     bloqueado_ate DATE, ts TIMESTAMPTZ DEFAULT now()
   );
   CREATE TABLE fila_revisar (
     id BIGSERIAL PRIMARY KEY, escola_id TEXT, assunto TEXT, corpo TEXT,
     anexo TEXT, status TEXT DEFAULT 'revisar', ts TIMESTAMPTZ DEFAULT now()
   );
   ```
4. Importe o fluxo: n8n → *Import from File* → `bot/n8n_orion_flow.json`.
5. Configure as credenciais no n8n (SMTP, Postgres, Header Auth p/ Evolution).
6. Ative o workflow.

## O que o fluxo faz
- **Agenda (seg–sex, 09–18, America/Sao_Paulo):** a cada hora busca escolas com toque devido.
- **Decide o toque** por `data_d0` → etapa **D0 / D4 / D7 / D14** e canal (e-mail/WhatsApp).
- **E-mail:** monta rascunho personalizado (variáveis `{nome_escola}`, `{nome_coordenacao}`,
  `{cidade}`) **com o PDF da apresentação anexado**. Se `EMAIL_MODO=draft` → grava em
  `fila_revisar`. Se `auto` **e** `aprovado=true` → envia via SMTP.
- **WhatsApp:** só se `wa_conversa_aberta=true`, dentro da janela 24h e `wa_toques < 2` → envia
  via Evolution API; senão pausa.
- **Opt-out (Webhook):** mensagem com palavra-chave → grava em `optout` com `bloqueado_ate = hoje+60d`
  e seta `status='opt-out'`.
- **Log:** toda ação grava em `eventos` e atualiza `status`/`data_atualizacao`.

## Anexar a apresentação
O PDF protegido (`docs/apresentacao_orion_protegido.pdf`) é anexado pelo nó *Montar e-mail*
via `ANEXO_APRESENTACAO`. Monte o volume no container do n8n para o caminho existir.

## Entregabilidade (importante)
Para e-mail não cair em spam, configure no domínio **SPF, DKIM e DMARC** do remetente e aqueça o
envio (volume baixo e crescente). Veja a nota de e-mail automático no resumo da operação.
