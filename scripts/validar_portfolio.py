from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"


class PortfolioParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag == "img":
            self.images.append((values.get("src", ""), values.get("alt", "")))


parser = PortfolioParser()
parser.feed(HTML.read_text(encoding="utf-8"))

required_ids = {"inicio", "projetos", "competencias", "sobre", "contato"}
missing_ids = required_ids - parser.ids
if missing_ids:
    raise SystemExit(f"Seções ausentes: {sorted(missing_ids)}")

for href in parser.links:
    if href.startswith("#") and href[1:] not in parser.ids:
        raise SystemExit(f"Âncora interna inexistente: {href}")
    parsed = urlparse(href)
    if parsed.scheme not in {"", "http", "https", "mailto"}:
        raise SystemExit(f"Protocolo inesperado: {href}")

for src, alt in parser.images:
    if not alt.strip():
        raise SystemExit(f"Imagem sem texto alternativo: {src}")
    if not (ROOT / src.split("?", 1)[0]).is_file():
        raise SystemExit(f"Imagem local ausente: {src}")

text = HTML.read_text(encoding="utf-8").lower()
if "catalogo-rpg" in text or "catálogo rpg" in text:
    raise SystemExit("O projeto cancelado não deve aparecer na página pública.")
if "conclusão prevista" in text or "formado em gestão da tecnologia da informação" not in text:
    raise SystemExit("A formação deve constar como concluída em 2025.")

print(f"Validação concluída: {len(parser.links)} links, {len(parser.images)} imagens e {len(parser.ids)} IDs.")
