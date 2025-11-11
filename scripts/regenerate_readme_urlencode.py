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

def extract_summary(p: Path, max_len: int = 140) -> str:
    """Extrae el primer párrafo de texto (ignorando headers) como resumen corto.
    Devuelve una cadena truncada y limpia, o cadena vacía si no hay resumen.
    """
    try:
        txt = p.read_text(encoding='utf-8')
    except Exception:
        return ''
    lines = txt.splitlines()
    # Skip initial title/header lines
    i = 0
    while i < len(lines) and lines[i].strip().startswith('#'):
        i += 1
    # Skip blank lines
    while i < len(lines) and not lines[i].strip():
        i += 1
    # Collect paragraph lines until blank or next header
    para_lines = []
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            break
        if line.lstrip().startswith('#'):
            break
        para_lines.append(line)
        i += 1
    if not para_lines:
        return ''
    para = ' '.join(ln.strip() for ln in para_lines)
    para = re.sub(r"\s+", ' ', para).strip()
    if len(para) > max_len:
        para = para[:max_len].rsplit(' ', 1)[0] + '...'
    return para

def extract_h2(p: Path) -> str:
    """Extrae el primer H2 como posible descripción breve."""
    try:
        txt = p.read_text(encoding='utf-8')
    except Exception:
        return ''
    m = re.search(r'^\s*##\s*(.+)', txt, re.M)
    if m:
        return clean_title(m.group(1))
    return ''

def extract_second_paragraph(p: Path, max_len: int = 140) -> str:
    """Extrae el segundo párrafo de texto (si existe) como fallback."""
    try:
        txt = p.read_text(encoding='utf-8')
    except Exception:
        return ''
    lines = txt.splitlines()
    # Find paragraphs (blocks of non-empty non-header lines)
    paras = []
    i = 0
    while i < len(lines):
        # skip headers
        if lines[i].strip().startswith('#'):
            i += 1
            continue
        # skip blank
        if not lines[i].strip():
            i += 1
            continue
        # collect paragraph
        buf = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#'):
            buf.append(lines[i].strip())
            i += 1
        paras.append(' '.join(buf))
    if len(paras) >= 2:
        para = re.sub(r"\s+", ' ', paras[1]).strip()
        if len(para) > max_len:
            para = para[:max_len].rsplit(' ', 1)[0] + '...'
        return para
    return ''

def prettify_filename(p: Path) -> str:
    s = p.stem.replace('-', ' ').replace('_', ' ')
    s = re.sub(r"\s+", ' ', s).strip()
    return s.capitalize()

def improve_summary(title: str, summary: str, p: Path, min_len: int = 30) -> str:
    """Si summary es vacío/pobre/idéntico al título, intenta mejorar con heurísticas."""
    if not summary:
        need = True
    else:
        ss = re.sub(r"\s+", ' ', summary).strip()
        need = len(ss) < min_len or ss.lower() == title.lower()
    if not need:
        return summary
    # Try H2
    h2 = extract_h2(p)
    if h2 and len(h2) >= min_len:
        return h2
    if h2:
        return h2
    # Try second paragraph
    sp = extract_second_paragraph(p)
    if sp:
        return sp
    # Fallback to prettified filename
    return prettify_filename(p)

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
        summary = extract_summary(p)
        summary = improve_summary(title, summary, p)
        sections.setdefault(cat, []).append((str(rel), title, summary))

    md = []
    md.append('# Índice del repositorio (enlaces corregidos)')
    md.append('Este README fue regenerado con rutas URL-encoded para asegurar que GitHub abra los archivos aunque contengan espacios o caracteres especiales.')
    md.append('')
    for cat in sorted(sections.keys()):
        md.append(f'## {cat.capitalize()}')
        md.append('')
        for rel, title, summary in sorted(sections[cat], key=lambda x: x[1].lower()):
            link = url_for(rel)
            safe = title.replace('\n',' ').strip()
            if summary:
                md.append(f'- [{safe}]({link}) — {summary}')
            else:
                md.append(f'- [{safe}]({link})')
        md.append('')

    out = ROOT / 'README.md'
    out.write_text('\n'.join(md), encoding='utf-8')
    print('Wrote README.md with', sum(len(v) for v in sections.values()), 'entries')

if __name__ == '__main__':
    main()
