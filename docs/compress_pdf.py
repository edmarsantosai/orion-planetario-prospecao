"""One-shot: recompacta imagens embutidas do PDF base da apresentacao.
Redimensiona fotos largas para ~150 DPI em A4 (<=1300px), JPEG q80.
Preserva: logo PNG transparente (alfa), vetores, texto e LINKS (anotacoes).
Uso: python docs/_tmp_compress_pdf.py
"""
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from PIL import Image

BASE = Path(__file__).resolve().parent
SRC = BASE / "apresentacao_orion.pdf"
OUT = BASE / "_tmp_light.pdf"
TARGET_W = 1300   # A4 210mm @ ~150 DPI = ~1240px
QUALITY = 80

def count_links(pdf):
    n = 0
    for p in pdf.pages:
        for a in (p.get("/Annots") or []):
            A = a.get_object().get("/A") or {}
            if A.get("/URI"):
                n += 1
    return n

def main():
    reader = PdfReader(str(SRC))
    writer = PdfWriter()
    writer.append(reader)

    COSMOS = (2, 3, 10)   # html,body background:#02030a — fundo real da pagina
    touched = skipped = 0
    for page in writer.pages:
        for img in page.images:
            try:
                im = img.image            # PIL Image
            except Exception:
                skipped += 1; continue
            w, h = im.size
            # logos / imagens pequenas com transparencia: manter intactas
            if w <= TARGET_W and im.mode in ("RGBA", "LA", "P"):
                skipped += 1; continue
            # fundos grandes RGBA: achatar sobre o cosmos (identico ao render)
            if im.mode in ("RGBA", "LA"):
                base = Image.new("RGB", im.size, COSMOS)
                base.paste(im, mask=im.getchannel("A"))
                im = base
            elif im.mode == "P":
                im = im.convert("RGB")
            elif im.mode != "RGB":
                im = im.convert("RGB")
            if w > TARGET_W:
                nh = round(h * TARGET_W / w)
                im = im.resize((TARGET_W, nh), Image.LANCZOS)
            img.replace(im, quality=QUALITY)
            touched += 1

    try:
        writer.compress_identical_objects()
    except Exception:
        pass

    with open(OUT, "wb") as fh:
        writer.write(fh)

    mb_src = SRC.stat().st_size / 1_048_576
    mb_out = OUT.stat().st_size / 1_048_576
    print(f"imagens recomprimidas: {touched} | puladas (logo/alfa): {skipped}")
    print(f"links URI preservados: base={count_links(reader)} -> novo={count_links(PdfReader(str(OUT)))}")
    print(f"tamanho: {mb_src:.2f} MB -> {mb_out:.2f} MB")

if __name__ == "__main__":
    main()
