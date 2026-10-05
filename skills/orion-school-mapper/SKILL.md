---
name: orion-school-mapper
description: Use ao mapear e priorizar escolas (SC e SP) para a prospecção Orion — define fontes, schema do Banco de Escolas, filtros de prioridade, dedupe e os guardrails de LGPD. Fase 1 da operação.
---

# orion-school-mapper

Como construir uma base limpa e priorizada de escolas com **dados de contato institucional**
para a operação Orion Planetários. Fonte de verdade das regras: `CLAUDE.md` §1, §2 e §4.

## Quando usar
- Ao iniciar/expandir `data/escolas_sc_sp.csv`.
- Ao enriquecer linhas existentes (telefone/site/instagram institucional).
- Antes de qualquer disparo da Fase 5 (o bot lê este CSV).

## Entradas
- Cidade-alvo (ver ordem em `CLAUDE.md` §4.1: SC = Balneário Camboriú, Itajaí, Florianópolis,
  Blumenau, Joinville, Brusque, Navegantes; SP = São Paulo, Campinas, Santos, Ribeirão Preto,
  São José dos Campos).
- Rede desejada (privada > pública), faixa de porte.

## Saídas
- `data/escolas_sc_sp.csv` (schema abaixo) + resumo quantitativo (nº por cidade, rede, prioridade).

## Fontes (e o que cada uma entrega de verdade)
| Fonte | Entrega | Limite |
|---|---|---|
| INEP / Censo Escolar (QEdu, educacaoja) | nome, rede, matrículas, etapas, endereço, cód. INEP | **não** tem contato nominal de diretor/coordenador |
| Google Perfil da Empresa (Maps/Search) | telefone institucional, site, nota, categoria | pode estar desatualizado |
| Site da escola | e-mail institucional, equipe pedagógica | varia muito |
| Instagram da escola | handle, engajamento, sinais de evento/planetário | sinal, não contato |
| Diretórios locais (imobiliárias/guias) | nomes de escolas por cidade, bairro, etapas | **validar** porte/contato na fonte primária |

## Schema (`data/escolas_sc_sp.csv`)
```
id,uf,cidade,nome_escola,rede,etapas,matriculas,cod_inep,
site,email_institucional,telefone_institucional,instagram,
seguidores_ig,nota_google,ja_teve_planetario,
nome_direcao,nome_coordenacao,fonte_contato,
prioridade,status,proximo_passo,data_atualizacao,observacoes
```
- `rede`: municipal | estadual | privada
- `etapas`: infantil;fundamental;medio (separar por `;`)
- `ja_teve_planetario`: sim | provavel | nao_identificado — **nunca inventar `nao`**
- `prioridade` (regra automática):
  - **P1** = privada com **200+ matrículas**
  - **P2** = bilíngue/premium (detectar por nome/IG/site)
  - **P3** = pública municipal/estadual de médio/grande porte (300+ matrículas)
- `status`: novo | contatado | conversa | proposta | fechado | descartado | opt-out
- `data_atualizacao`: ISO `AAAA-MM-DD`

## Execução
1. Puxar base INEP/QEdu por cidade → nome, rede, matrículas, etapas, cód. INEP.
2. Enriquecer com Google Perfil + site + Instagram (telefone, e-mail, handle, sinais).
3. **Nome de direção/coordenação:** deixar vazio; preencher só via **ligação humana** (passo 1).
4. Aplicar filtros e calcular `prioridade`. Dedupe por `cod_inep` (ou nome+cidade se INEP ausente).
5. Preencher só o que for verificável; o que faltar → vazio ou `[VALIDAR COM A ORION]`. Nunca chutar.
6. Entregar CSV + resumo quantitativo.

## GUARDRAILS (inegociáveis — `CLAUDE.md` §2)
- **LGPD:** só dados de **canais institucionais públicos**. Proibido coletar/usar celular ou
  WhatsApp **pessoal** de diretor/coordenador obtido de forma não pública.
- Respeitar robots.txt e termos de cada fonte; **sem scraping agressivo** de rede social.
- Contato pessoal nominal entra **só** pela ligação humana (passo 1), nunca por raspagem.
- Dado ausente = campo vazio ou `[VALIDAR COM A ORION]`, jamais achismo.

## Nota de estado (2026-10-05)
Lote-semente atual: 21 escolas privadas de SC (Balneário Camboriú, Itajaí, Florianópolis),
com contatos/matrículas a coletar. Próximos lotes: Blumenau, Joinville + capitais SP.
