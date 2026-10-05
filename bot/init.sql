-- Schema inicial do Orion Outreach Bot (criado no 1o boot do Postgres)
CREATE TABLE IF NOT EXISTS escolas (
  id TEXT PRIMARY KEY,
  uf TEXT, cidade TEXT, nome_escola TEXT, rede TEXT,
  email_institucional TEXT, telefone_institucional TEXT, instagram TEXT,
  nome_coordenacao TEXT, prioridade TEXT,
  status TEXT DEFAULT 'novo',            -- novo|contatado|conversa|proposta|fechado|descartado|opt-out
  aprovado BOOLEAN DEFAULT false,        -- true = pode enviar e-mail automatico
  wa_conversa_aberta BOOLEAN DEFAULT false,
  wa_ultimo_inbound TIMESTAMPTZ,         -- janela 24h
  wa_toques INT DEFAULT 0,
  data_d0 DATE,                          -- inicio da cadencia
  proximo_passo TEXT,
  data_atualizacao DATE
);

CREATE TABLE IF NOT EXISTS eventos (
  id BIGSERIAL PRIMARY KEY,
  escola_id TEXT REFERENCES escolas(id),
  canal TEXT, etapa TEXT, acao TEXT, detalhe TEXT,
  ts TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS optout (
  escola_id TEXT PRIMARY KEY,
  motivo TEXT, bloqueado_ate DATE,
  ts TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS fila_revisar (
  id BIGSERIAL PRIMARY KEY,
  escola_id TEXT, assunto TEXT, corpo TEXT, anexo TEXT,
  status TEXT DEFAULT 'revisar',         -- revisar|aprovado|enviado|descartado
  ts TIMESTAMPTZ DEFAULT now()
);

-- Import da base: copie data/escolas_sc_sp.csv e rode \copy mapeando as colunas
-- usadas aqui (id,uf,cidade,nome_escola,rede,prioridade). Depois defina data_d0
-- e aprovado=true nas escolas liberadas para envio automatico.
