#!/usr/bin/env python3
"""
Regenera README.md asegurando que los enlaces a archivos locales estén URL-encoded
para evitar problemas con espacios/caracteres especiales en GitHub.

Escribe `README.md` en la raíz y no deja otros archivos temporales.
"""
from pathlib import Path
import re
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
PENT = ROOT / 'pentesting'

def clean_title(s: str) -> str:
    s = s.strip()
    s = re.sub(r"^#{1,6}\s*", '', s)
    s = re.sub(r"\s+", ' ', s)
    return s

def extract_title(p: Path) -> str:
    try:
        txt = p.read_text(encoding='utf-8')
    except Exception:
        return p.stem
    m = re.search(r'^\s*#\s*(.+)', txt, re.M)
    if m:
        return clean_title(m.group(1))
    # fallback first non-empty line
    for line in txt.splitlines():
        if line.strip():
            return clean_title(line.strip())
    return p.stem

def url_for(rel_path: str) -> str:
    # GitHub expects paths with spaces encoded as %20; quote the path but keep slashes
    parts = rel_path.split('/')
    return '/'.join(quote(p) for p in parts)

def main():
    if not PENT.exists():
        print('No pentesting/ dir found')
        return
    sections = {}
    for p in sorted(PENT.rglob('*.md')):
        rel = p.relative_to(ROOT)
        parts = rel.parts
        cat = parts[1] if len(parts) > 1 else 'root'
        title = extract_title(p)
        sections.setdefault(cat, []).append((str(rel), title))

    md = []
    md.append('# Índice del repositorio (enlaces corregidos)')
    md.append('Este README fue regenerado con rutas URL-encoded para asegurar que GitHub abra los archivos aunque contengan espacios o caracteres especiales.')
    md.append('')
    for cat in sorted(sections.keys()):
        md.append(f'## {cat.capitalize()}')
        md.append('')
        for rel, title in sorted(sections[cat], key=lambda x: x[1].lower()):
            link = url_for(rel)
            safe = title.replace('\n',' ').strip()
            md.append(f'- [{safe}]({link})')
        md.append('')

    out = ROOT / 'README.md'
    out.write_text('\n'.join(md), encoding='utf-8')
    print('Wrote README.md with', sum(len(v) for v in sections.values()), 'entries')

if __name__ == '__main__':
    main()
