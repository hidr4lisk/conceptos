#!/usr/bin/env python3
"""
Genera RENAME_SUGGESTIONS.md con propuestas de nombres legibles para archivos Markdown
basado en el primer header H1 del archivo. Escanea la carpeta `pentesting/` recursivamente.

Salida: crea (o sobreescribe) `RENAME_SUGGESTIONS.md` en la raíz del repo con líneas:

    ruta/actual.md -> Nombre Propuesto.md

Las propuestas intentan:
 - usar el H1 completo si existe, limpiando caracteres no válidos para filenames
 - truncar a 80 caracteres si es necesario
 - evitar conflictos simples (agregar sufijo incremental si el nombre ya está propuesto)

Usar con: python3 scripts/generate_rename_suggestions.py
"""
import re
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
PENTEST = ROOT / 'pentesting'

def slugify_name(name: str) -> str:
    # Normalize and remove control chars
    name = unicodedata.normalize('NFKD', name)
    name = name.strip()
    # Replace newlines and excessive whitespace
    name = re.sub(r"\s+", " ", name)
    # Remove characters not suitable for filenames but keep common punctuation
    name = re.sub(r"[\\/:*?\"<>|]", '', name)
    # Limit length
    if len(name) > 80:
        name = name[:77].rstrip() + '...'
    return name

def extract_h1(file_path: Path) -> str:
    try:
        with file_path.open('r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # H1 as '# Title' or first non-empty line if header missing
                m = re.match(r'^#\s+(.*)', line)
                if m:
                    return m.group(1).strip()
                # fallback to first non-empty line
                return line
    except Exception:
        return ''

def propose_filename(title: str, ext: str = '.md') -> str:
    if not title:
        return 'untitled' + ext
    clean = slugify_name(title)
    # Replace spaces with ' - ' for readability
    filename = clean.replace(' ', ' - ')
    filename = filename + ext
    return filename

def main():
    md_files = sorted([p for p in PENTEST.rglob('*.md') if p.is_file()])
    suggestions = []
    used = {}
    for p in md_files:
        rel = p.relative_to(ROOT)
        title = extract_h1(p)
        prop = propose_filename(title)
        # avoid duplicate proposed filenames
        base = prop
        i = 1
        while prop in used:
            i += 1
            name_no_ext = base[:-3]
            prop = f"{name_no_ext} ({i}){base[-3:]}"
        used[prop] = str(rel)
        suggestions.append((str(rel), title or '', prop))

    out = ROOT / 'RENAME_SUGGESTIONS.md'
    with out.open('w', encoding='utf-8') as f:
        f.write('# RENAME_SUGGESTIONS\n')
        f.write('\n')
        f.write('Ruta actual -> Título extraído -> Nombre propuesto\n\n')
        for src, title, prop in suggestions:
            f.write(f'- `{src}` -> `{title}` -> `{prop}`\n')

    print(f'Wrote {out} with {len(suggestions)} suggestions')

if __name__ == '__main__':
    main()
