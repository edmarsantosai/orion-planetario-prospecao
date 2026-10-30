# Envio manual do e-mail Orion (HTML no corpo)

> Para disparo **manual** (sem Make), 1 a 1, com o template pronto `docs/apresentacao_email.html`.
> Use isto para as escolas quentes/Tier 1 e 2, onde vale o toque personalizado.
> **Regra de compliance:** 1º toque frio é **ligação** — o e-mail entra como reforço/registro depois de falar (ou para contato institucional público). Opt-out ("sair") = encerrar por 60 dias.

---

## 1. Arquivo do template
`docs/apresentacao_email.html` — abre no navegador (duplo-clique) e renderiza o e-mail completo.
As imagens ficam hospedadas em `orionplanetarios.com.br` (NÃO anexar imagem — piora a entrega).

## 2. Assunto (escolha 1 — < 50 caracteres, sem gatilho de spam)
- `Um planetário 360° na {NOME_ESCOLA}?`
- `Ideia para a escola em {CIDADE}: planetário na sala`
- `{NOME_COORDENACAO}, 15 min sobre astronomia na escola?`

> Nunca use "Re:"/"Fwd:" no 1º contato, nem CAIXA ALTA, nem "grátis/garantido/promoção".

## 3. Os 3 campos para personalizar antes de enviar
| Campo no HTML | Preencher com | Se não souber |
|---|---|---|
| `{{NOME_COORDENACAO}}` | nome da coordenação/direção (pego na ligação) | `equipe pedagógica` |
| `{{NOME_ESCOLA}}` | nome da escola | (sempre preencher) |
| `{{CIDADE}}` | cidade da escola | (sempre preencher) |

## 4. Como colar o HTML no corpo (2 formas)

### Opção A — Thunderbird (melhor fidelidade, grátis) ⭐ recomendada
1. Conta: `comercial@edmarsantos.com.br` · SMTP `srv252.prodns.com.br:465 SSL`.
2. Escrever → menu **Inserir → HTML**.
3. Cole o **código-fonte** do `apresentacao_email.html` (já com os 3 campos trocados) → OK.
4. Confira o assunto, o Reply-To e o BCC (abaixo) → Enviar.

### Opção B — Gmail / webmail (cola do navegador)
1. Abra `apresentacao_email.html` no **Chrome/Edge** (duplo-clique).
2. `Ctrl+A` → `Ctrl+C`.
3. Na janela de compor, `Ctrl+V` — cola o visual renderizado (layout, cores, botão, imagens).
4. **Edite direto no corpo** os 3 pontos em negrito (nome, escola, cidade). No Gmail dá para clicar e digitar por cima.
   > O Gmail só cola o **resultado visual** do navegador — não aceita colar código `<html>` cru.

## 5. Cabeçalhos a configurar (iguais à campanha automática)
- **De:** `comercial@edmarsantos.com.br` (SPF/DKIM alinhados — manter)
- **Responder para (Reply-To):** `edmar.orionplanetarios@gmail.com` (respostas caem no seu Gmail)
- **Cco (BCC):** `edmarsantos.unasp@gmail.com` e `edmar.orionplanetarios@gmail.com` (cópia oculta de cada envio)

## 6. Teste antes de escalar
Mande 1 e-mail de teste para 1 Gmail + 1 Outlook e confira: **não caiu em spam** e **as imagens carregam** sem clicar em "exibir imagens".

## 7. Onde registrar o envio
Marcar `status = contatado` e `data_atualizacao` na escola, no hub do Notion (links abaixo).

---

## Links do Hub de Prospecção (Notion)
- 🌌 **Hub do Representante:** https://www.notion.so/3be6bedf1e1f811eb818f65bee2fc05f
- 🏫 **Banco de Escolas — Master (SC·SP·PR):** https://www.notion.so/5ffae69b9dd3476a8eeb290ff1740e03
