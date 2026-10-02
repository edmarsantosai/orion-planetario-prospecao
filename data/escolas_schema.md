# Schema — Banco de Escolas (espelha o Notion DB `Banco de Escolas — SC/SP`)

> **Master = Notion** (`collection://34769498-7cbc-481a-9feb-ba8943010c2e`).
> Este arquivo documenta os campos. O CSV é só export/seed **sem dado pessoal** (LGPD).

| Campo | Tipo | Valores / regra |
|---|---|---|
| `nome_escola` | título | nome institucional |
| `uf` | select | SC \| SP |
| `cidade` | select | cidade-alvo |
| `rede` | select | municipal \| estadual \| privada |
| `etapas` | multi | Infantil \| Fund I \| Fund II \| Médio |
| `matriculas` | número | nº de alunos |
| `cod_inep` | texto | código INEP (dedupe por aqui) |
| `site` | url | — |
| `email_institucional` | email | só canal público |
| `telefone_institucional` | telefone | só canal público |
| `instagram` | texto | handle |
| `seguidores_ig` | número | — |
| `nota_google` | número | 0–5 |
| `ja_teve_planetario` | select | sim \| provável \| não identificado (nunca "não") |
| `qual_planetario` | texto | resposta de "qual planetário já receberam?" |
| `nome_direcao` | texto | **DADO PESSOAL — só no Notion, nunca no Git** |
| `nome_coordenacao` | texto | **DADO PESSOAL — só no Notion, nunca no Git** |
| `fonte_contato` | select | ligação \| site \| maps \| instagram \| indicação |
| `prioridade` | select | P1 (privada 200+) \| P2 (bilíngue/premium) \| P3 (pública 300+) |
| `status` | select | Novo \| Contatado \| Conversa \| Proposta \| Fechado \| Descartado \| Opt-out |
| `proximo_passo` | texto | — |
| `follow_up` | data | ISO aaaa-mm-dd |
| `opt_out_ate` | data | opt-out bloqueia 60 dias |
| `observacoes` | texto | — |
| `data_atualizacao` | last edited | automático |

## Regras
- **Dedupe** por `cod_inep`.
- `prioridade` automática: P1 = privada 200+ matrículas; P2 = bilíngue/premium; P3 = pública 300+.
- Nomes de direção/coordenação **só via ligação humana** (Passo 1) e **só no Notion**.
- O bot (n8n) lê/escreve direto no Notion DB via API — o CSV não é fonte de estado.
