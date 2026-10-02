"""
Gera a versão PROTEGIDA do PDF da apresentação Orion.
- Bloqueia: copiar texto/imagem, editar, extrair conteúdo.
- Permite: abrir sem senha e imprimir.

Observação honesta: a proteção de PDF é uma restrição de PERMISSÃO (senha de dono).
Leitores que respeitam o padrão (Adobe, Edge, Chrome, Foxit) bloqueiam copiar/editar,
mas o conteúdo continua visível — não é criptografia à prova de tudo.

Uso:
    python docs/build_pdf.py
Pré-requisito do PDF base (docs/apresentacao_orion.pdf) — gerar com Edge headless:
    msedge --headless=new --no-pdf-header-footer --virtual-time-budget=12000 \
      --print-to-pdf="docs/apresentacao_orion.pdf" \
      "file:///CAMINHO/docs/apresentacao_orion.html"
"""
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions as UAP

BASE = Path(__file__).resolve().parent
SRC = BASE / "apresentacao_orion.pdf"
OUT = BASE / "apresentacao_orion_protegido.pdf"
OWNER_PASSWORD = "orion-edmar-2026"  # senha de dono (troque se quiser)

def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"PDF base nao encontrado: {SRC}\nGere primeiro com Edge headless (ver cabecalho).")

    reader = PdfReader(str(SRC))
    writer = PdfWriter()
    writer.append(reader)

    # Permite SO imprimir (inclusive alta resolucao). Copiar/editar/extrair = bloqueados.
    perms = UAP.PRINT | UAP.PRINT_TO_REPRESENTATION

    writer.encrypt(
        user_password="",            # abre sem senha
        owner_password=OWNER_PASSWORD,
        permissions_flag=perms,
        algorithm="AES-256",
    )
    with open(OUT, "wb") as fh:
        writer.write(fh)
    print(f"OK -> {OUT}")

if __name__ == "__main__":
    main()
